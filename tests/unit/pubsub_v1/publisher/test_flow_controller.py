# Copyright 2020, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import threading
import warnings

import pytest

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher.flow_controller import FlowController


def test_no_overflow_no_error():
    settings = types.PublishFlowControl(
        message_limit=100,
        byte_limit=10000,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    # there should be no errors
    for data in (b"foo", b"bar", b"baz"):
        msg = types.PubsubMessage(data=data)
        instance.add(msg)


def test_overflow_no_error_on_ignore():
    settings = types.PublishFlowControl(
        message_limit=1,
        byte_limit=2,
        limit_exceeded_behavior=types.LimitExceededBehavior.IGNORE,
    )
    instance = FlowController(settings)

    # there should be no overflow errors
    instance.add(types.PubsubMessage(data=b"foo"))
    instance.add(types.PubsubMessage(data=b"bar"))


def test_message_count_overflow_error():
    settings = types.PublishFlowControl(
        message_limit=1,
        byte_limit=10000,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    instance.add(types.PubsubMessage(data=b"foo"))
    with pytest.raises(exceptions.FlowControlLimitError) as error:
        instance.add(types.PubsubMessage(data=b"bar"))

    assert "messages: 2 / 1" in str(error.value)


def test_byte_size_overflow_error():
    settings = types.PublishFlowControl(
        message_limit=10000,
        byte_limit=199,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    # Since the message data itself occupies 100 bytes, it means that both
    # messages combined will exceed the imposed byte limit of 199, but a single
    # message will not (the message size overhead is way lower than data size).
    msg1 = types.PubsubMessage(data=b"x" * 100)
    msg2 = types.PubsubMessage(data=b"y" * 100)

    instance.add(msg1)
    with pytest.raises(exceptions.FlowControlLimitError) as error:
        instance.add(msg2)

    total_size = msg1.ByteSize() + msg2.ByteSize()
    expected_info = "bytes: {} / 199".format(total_size)
    assert expected_info in str(error.value)


def test_no_error_on_moderate_message_flow():
    settings = types.PublishFlowControl(
        message_limit=2,
        byte_limit=250,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    msg1 = types.PubsubMessage(data=b"x" * 100)
    msg2 = types.PubsubMessage(data=b"y" * 100)
    msg3 = types.PubsubMessage(data=b"z" * 100)

    # The flow control settings will accept two in-flight messages, but not three.
    # If releasing messages works correctly, the sequence below will not raise errors.
    instance.add(msg1)
    instance.add(msg2)
    instance.release(msg1)
    instance.add(msg3)
    instance.release(msg2)
    instance.release(msg3)


def test_rejected_messages_do_not_increase_total_load():
    settings = types.PublishFlowControl(
        message_limit=1,
        byte_limit=150,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    msg1 = types.PubsubMessage(data=b"x" * 100)
    msg2 = types.PubsubMessage(data=b"y" * 100)

    instance.add(msg1)

    for _ in range(5):
        with pytest.raises(exceptions.FlowControlLimitError):
            instance.add(types.PubsubMessage(data=b"z" * 100))

    # After releasing a message we should again be able to add another one, despite
    # previously trying to add a lot of other messages.
    instance.release(msg1)
    instance.add(msg2)


def test_incorrectly_releasing_too_many_messages():
    settings = types.PublishFlowControl(
        message_limit=1,
        byte_limit=150,
        limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
    )
    instance = FlowController(settings)

    msg1 = types.PubsubMessage(data=b"x" * 100)
    msg2 = types.PubsubMessage(data=b"y" * 100)
    msg3 = types.PubsubMessage(data=b"z" * 100)

    # Releasing a message that would make the load negative should result in a warning.
    with warnings.catch_warnings(record=True) as warned:
        instance.release(msg1)

    assert len(warned) == 1
    assert issubclass(warned[0].category, RuntimeWarning)
    warning_msg = str(warned[0].message)
    assert "never added or already released" in warning_msg

    # Incorrectly removing a message does not mess up internal stats, we can
    # still only add a single message at a time to this flow.
    instance.add(msg2)

    with pytest.raises(exceptions.FlowControlLimitError) as error:
        instance.add(msg3)

    error_msg = str(error.value)
    assert "messages: 2 / 1" in error_msg
    total_size = msg2.ByteSize() + msg3.ByteSize()
    expected_size_info = "bytes: {} / 150".format(total_size)
    assert expected_size_info in error_msg


def test_blocking_on_overflow_until_free_capacity():
    settings = types.PublishFlowControl(
        message_limit=2,
        byte_limit=250,
        limit_exceeded_behavior=types.LimitExceededBehavior.BLOCK,
    )
    instance = FlowController(settings)

    msg1 = types.PubsubMessage(data=b"x" * 100)
    msg2 = types.PubsubMessage(data=b"y" * 100)
    msg3 = types.PubsubMessage(data=b"z" * 100)
    msg4 = types.PubsubMessage(data=b"w" * 100)

    # If there is a concurrency bug in FlowController, we do not want to block
    # the main thread running the tests, thus we delegate all add/release
    # operations to daemon threads.
    adding_123_done = threading.Event()
    adding_4_done = threading.Event()
    releasing_12_done = threading.Event()

    def add_messages(messages, all_done_event):
        try:
            for msg in messages:
                instance.add(msg)
        except Exception:
            return
        else:
            all_done_event.set()

    def release_messages(messages, all_done_event):
        try:
            for msg in messages:
                instance.release(msg)
        except Exception:
            return
        else:
            all_done_event.set()

    # The thread should block on adding the 3rd message.
    adder_thread_123 = threading.Thread(
        target=add_messages, args=([msg1, msg2, msg3], adding_123_done)
    )
    adder_thread_123.daemon = True
    adder_thread_123.start()

    all_added = adding_123_done.wait(timeout=0.1)
    if all_added:
        pytest.fail("Adding a message on overflow did not block.")

    # Start adding another message, but in the meantime also start freeing up
    # enough flow capacity for it.
    adder_thread_4 = threading.Thread(target=add_messages, args=([msg4], adding_4_done))
    adder_thread_4.daemon = True
    adder_thread_4.start()

    releaser_thread = threading.Thread(
        target=release_messages, args=([msg1, msg2], releasing_12_done)
    )
    releaser_thread.daemon = True
    releaser_thread.start()

    all_released = releasing_12_done.wait(timeout=0.1)
    if not all_released:
        pytest.fail("Releasing messages blocked or errored.")

    # After releasing two messages, adding a new one (msg4) should not block, even
    # if msg3 has not been released yet.
    all_added = adding_4_done.wait(timeout=0.1)
    if not all_added:
        pytest.fail("Adding a message with enough flow capacity blocked or errored.")
