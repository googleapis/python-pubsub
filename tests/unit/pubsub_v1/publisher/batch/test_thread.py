# Copyright 2017, Google LLC All rights reserved.
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

import datetime
import sys
import threading
import time

# special case python < 3.8
if sys.version_info.major == 3 and sys.version_info.minor < 8:
    import mock
else:
    from unittest import mock

import pytest

from opentelemetry import trace

import google.api_core.exceptions
from google.api_core import gapic_v1
from google.auth import credentials
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher._batch.base import BatchStatus
from google.cloud.pubsub_v1.publisher._batch.base import BatchCancellationReason
from google.cloud.pubsub_v1.publisher._batch import thread
from google.cloud.pubsub_v1.publisher._batch.thread import Batch
from google.pubsub_v1 import types as gapic_types
from google.cloud.pubsub_v1.opentelemetry.publish_message_wrapper import (
    PublishMessageWrapper,
)


def create_client(enable_open_telemetry=False):
    return publisher.Client(
        credentials=credentials.AnonymousCredentials(),
        publisher_options=types.PublisherOptions(
            enable_open_telemetry_tracing=enable_open_telemetry,
        ),
    )


def create_batch(
    topic="topic_name",
    batch_done_callback=None,
    commit_when_full=True,
    commit_retry=gapic_v1.method.DEFAULT,
    commit_timeout: gapic_types.TimeoutType = gapic_v1.method.DEFAULT,
    enable_open_telemetry: bool = False,
    **batch_settings,
):
    """Return a batch object suitable for testing.

    Args:
        topic (str): Topic name.
        batch_done_callback (Callable[bool]): A callable that is called when
            the batch is done, either with a success or a failure flag.
        commit_when_full (bool): Whether to commit the batch when the batch
            has reached byte-size or number-of-messages limits.
        commit_retry (Optional[google.api_core.retry.Retry]): The retry settings
            for the batch commit call.
        commit_timeout (:class:`~.pubsub_v1.types.TimeoutType`):
            The timeout to apply to the batch commit call.
        batch_settings (Mapping[str, str]): Arguments passed on to the
            :class:``~.pubsub_v1.types.BatchSettings`` constructor.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Batch: A batch object.
    """
    client = create_client(enable_open_telemetry=enable_open_telemetry)
    settings = types.BatchSettings(**batch_settings)
    return Batch(
        client,
        topic,
        settings,
        batch_done_callback=batch_done_callback,
        commit_when_full=commit_when_full,
        commit_retry=commit_retry,
        commit_timeout=commit_timeout,
    )


@mock.patch.object(threading, "Lock")
def test_make_lock(Lock):
    lock = Batch.make_lock()
    assert lock is Lock.return_value
    Lock.assert_called_once_with()


def test_client():
    client = create_client()
    settings = types.BatchSettings()
    batch = Batch(client, "topic_name", settings)
    assert batch.client is client


def test_commit():
    batch = create_batch()

    with mock.patch.object(
        Batch, "_start_commit_thread", autospec=True
    ) as _start_commit_thread:
        batch.commit()
        _start_commit_thread.assert_called_once()

    # The batch's status needs to be something other than "accepting messages",
    # since the commit started.
    assert batch.status != BatchStatus.ACCEPTING_MESSAGES
    assert batch.status == BatchStatus.STARTING


def test_commit_no_op():
    batch = create_batch()
    batch._status = BatchStatus.IN_PROGRESS
    with mock.patch.object(threading, "Thread", autospec=True) as Thread:
        batch.commit()

    # Make sure a thread was not created.
    Thread.assert_not_called()

    # Check that batch status is unchanged.
    assert batch.status == BatchStatus.IN_PROGRESS


def test_blocking__commit():
    batch = create_batch()
    futures = (
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"This is my message."),
                span=None,
            )
        ),
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"This is another message."),
                span=None,
            )
        ),
    )

    # Set up the underlying API publish method to return a PublishResponse.
    publish_response = gapic_types.PublishResponse(message_ids=["a", "b"])
    patch = mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    )
    with patch as publish:
        batch._commit()

    # Establish that the underlying API call was made with expected
    # arguments.
    publish.assert_called_once_with(
        topic="topic_name",
        messages=[
            gapic_types.PubsubMessage(data=b"This is my message."),
            gapic_types.PubsubMessage(data=b"This is another message."),
        ],
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
    )

    # Establish that all of the futures are done, and that they have the
    # expected values.
    assert futures[0].done()
    assert futures[0].result() == "a"
    assert futures[1].done()
    assert futures[1].result() == "b"


def test_blocking__commit_custom_retry():
    batch = create_batch(commit_retry=mock.sentinel.custom_retry)
    batch.publish(
        message_wrapper=PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"This is my message."),
            span=None,
        )
    )

    # Set up the underlying API publish method to return a PublishResponse.
    publish_response = gapic_types.PublishResponse(message_ids=["a"])
    patch = mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    )
    with patch as publish:
        batch._commit()

    # Establish that the underlying API call was made with expected
    # arguments.
    publish.assert_called_once_with(
        topic="topic_name",
        messages=[gapic_types.PubsubMessage(data=b"This is my message.")],
        retry=mock.sentinel.custom_retry,
        timeout=gapic_v1.method.DEFAULT,
    )


def test_blocking__commit_custom_timeout():
    batch = create_batch(commit_timeout=mock.sentinel.custom_timeout)
    batch.publish(
        message_wrapper=PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"This is my message."),
            span=None,
        )
    )

    # Set up the underlying API publish method to return a PublishResponse.
    publish_response = gapic_types.PublishResponse(message_ids=["a"])
    patch = mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    )
    with patch as publish:
        batch._commit()

    # Establish that the underlying API call was made with expected
    # arguments.
    publish.assert_called_once_with(
        topic="topic_name",
        messages=[gapic_types.PubsubMessage(data=b"This is my message.")],
        retry=gapic_v1.method.DEFAULT,
        timeout=mock.sentinel.custom_timeout,
    )


def test_client_api_publish_not_blocking_additional_publish_calls():
    batch = create_batch(max_messages=1)
    api_publish_called = threading.Event()

    def api_publish_delay(topic="", messages=(), retry=None, timeout=None):
        api_publish_called.set()
        time.sleep(1.0)
        message_ids = [str(i) for i in range(len(messages))]
        return gapic_types.PublishResponse(message_ids=message_ids)

    api_publish_patch = mock.patch.object(
        type(batch.client), "_gapic_publish", side_effect=api_publish_delay
    )

    with api_publish_patch:
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"first message"),
                span=None,
            )
        )

        start = datetime.datetime.now()
        event_set = api_publish_called.wait(timeout=1.0)
        if not event_set:  # pragma: NO COVER
            pytest.fail("API publish was not called in time")
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"second message"),
                span=None,
            )
        )
        end = datetime.datetime.now()

    # While a batch commit in progress, waiting for the API publish call to
    # complete should not unnecessariliy delay other calls to batch.publish().
    assert (end - start).total_seconds() < 1.0


@mock.patch.object(thread, "_LOGGER")
def test_blocking__commit_starting(_LOGGER):
    batch = create_batch()
    batch._status = BatchStatus.STARTING

    batch._commit()
    assert batch._status == BatchStatus.SUCCESS

    _LOGGER.debug.assert_called_once_with("No messages to publish, exiting commit")


@mock.patch.object(thread, "_LOGGER")
def test_blocking__commit_already_started(_LOGGER):
    batch = create_batch()
    batch._status = BatchStatus.IN_PROGRESS

    batch._commit()
    assert batch._status == BatchStatus.IN_PROGRESS

    _LOGGER.debug.assert_called_once_with(
        "Batch is already in progress or has been cancelled, exiting commit"
    )


def test_blocking__commit_no_messages():
    batch = create_batch()
    with mock.patch.object(type(batch.client), "_gapic_publish") as publish:
        batch._commit()

    assert publish.call_count == 0


def test_blocking__commit_wrong_messageid_length():
    batch = create_batch()
    futures = (
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah"),
                span=None,
            )
        ),
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah blah"),
                span=None,
            )
        ),
    )

    # Set up a PublishResponse that only returns one message ID.
    publish_response = gapic_types.PublishResponse(message_ids=["a"])
    patch = mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    )

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert isinstance(future.exception(), exceptions.PublishError)


def test_block__commmit_api_error():
    batch = create_batch()
    futures = (
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah"),
                span=None,
            )
        ),
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah blah"),
                span=None,
            )
        ),
    )

    # Make the API throw an error when publishing.
    error = google.api_core.exceptions.InternalServerError("uh oh")
    patch = mock.patch.object(type(batch.client), "_gapic_publish", side_effect=error)

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert future.exception() == error


def test_block__commmit_retry_error():
    batch = create_batch()
    futures = (
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah"),
                span=None,
            )
        ),
        batch.publish(
            message_wrapper=PublishMessageWrapper(
                message=gapic_types.PubsubMessage(data=b"blah blah blah blah"),
                span=None,
            )
        ),
    )

    # Make the API throw an error when publishing.
    error = google.api_core.exceptions.RetryError("uh oh", None)
    patch = mock.patch.object(type(batch.client), "_gapic_publish", side_effect=error)

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert future.exception() == error


def test_publish_updating_batch_size():
    batch = create_batch(topic="topic_foo")
    messages = (
        PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"foobarbaz"), span=None
        ),
        PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"spameggs"), span=None
        ),
        PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"1335020400"), span=None
        ),
    )

    # Publish each of the messages, which should save them to the batch.
    futures = [batch.publish(message) for message in messages]

    # There should be three messages on the batch, and three futures.
    assert len(batch.message_wrappers) == 3
    assert batch._futures == futures

    # The size should have been incremented by the sum of the size
    # contributions of each message to the PublishRequest.
    base_request_size = gapic_types.PublishRequest(topic="topic_foo")._pb.ByteSize()
    expected_request_size = base_request_size + sum(
        gapic_types.PublishRequest(messages=[msg.message])._pb.ByteSize()
        for msg in messages
    )

    assert batch.size == expected_request_size
    assert batch.size > 0  # I do not always trust protobuf.


def test_publish():
    batch = create_batch()
    wrapper = PublishMessageWrapper(gapic_types.PubsubMessage(), None)
    future = batch.publish(wrapper)

    assert len(batch.message_wrappers) == 1
    assert batch._futures == [future]


def test_publish_max_messages_zero():
    batch = create_batch(topic="topic_foo", max_messages=0)

    wrapper = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    with mock.patch.object(batch, "commit") as commit:
        future = batch.publish(wrapper)

    assert future is not None
    assert len(batch.message_wrappers) == 1
    assert batch._futures == [future]
    commit.assert_called_once()


def test_publish_max_messages_enforced():
    batch = create_batch(topic="topic_foo", max_messages=1)

    message = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    message2 = PublishMessageWrapper(
        gapic_types.PubsubMessage(data=b"foobarbaz2"), None
    )

    future = batch.publish(message)
    future2 = batch.publish(message2)

    assert future is not None
    assert future2 is None
    assert len(batch.message_wrappers) == 1
    assert len(batch._futures) == 1


def test_publish_max_bytes_enforced():
    batch = create_batch(topic="topic_foo", max_bytes=15)

    message = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    message2 = PublishMessageWrapper(
        gapic_types.PubsubMessage(data=b"foobarbaz2"), None
    )

    future = batch.publish(message)
    future2 = batch.publish(message2)

    assert future is not None
    assert future2 is None
    assert len(batch.message_wrappers) == 1
    assert len(batch._futures) == 1


def test_publish_exceed_max_messages():
    max_messages = 4
    batch = create_batch(max_messages=max_messages)
    messages = (
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None),
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"spameggs"), None),
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"1335020400"), None),
    )

    # Publish each of the messages, which should save them to the batch.
    with mock.patch.object(batch, "commit") as commit:
        futures = [batch.publish(message) for message in messages]
        assert batch._futures == futures
        assert len(futures) == max_messages - 1

        # Commit should not yet have been called.
        assert commit.call_count == 0

        # When a fourth message is published, commit should be called.
        # No future will be returned in this case.
        future = batch.publish(
            PublishMessageWrapper(gapic_types.PubsubMessage(data=b"last one"), None)
        )
        commit.assert_called_once_with()

        assert future is None
        assert batch._futures == futures


@mock.patch.object(thread, "_SERVER_PUBLISH_MAX_BYTES", 1000)
def test_publish_single_message_size_exceeds_server_size_limit():
    batch = create_batch(
        topic="topic_foo",
        max_messages=1000,
        max_bytes=1000 * 1000,  # way larger than (mocked) server side limit
    )

    big_message = gapic_types.PubsubMessage(data=b"x" * 984)

    request_size = gapic_types.PublishRequest(
        topic="topic_foo", messages=[big_message]
    )._pb.ByteSize()
    assert request_size == 1001  # sanity check, just above the (mocked) server limit

    with pytest.raises(exceptions.MessageTooLargeError):
        batch.publish(PublishMessageWrapper(big_message, None))


@mock.patch.object(thread, "_SERVER_PUBLISH_MAX_BYTES", 1000)
def test_publish_total_messages_size_exceeds_server_size_limit():
    batch = create_batch(topic="topic_foo", max_messages=10, max_bytes=1500)

    messages = (
        gapic_types.PubsubMessage(data=b"x" * 500),
        gapic_types.PubsubMessage(data=b"x" * 600),
    )

    # Sanity check - request size is still below BatchSettings.max_bytes,
    # but it exceeds the server-side size limit.
    request_size = gapic_types.PublishRequest(
        topic="topic_foo", messages=messages
    )._pb.ByteSize()
    assert 1000 < request_size < 1500

    with mock.patch.object(batch, "commit") as fake_commit:
        batch.publish(PublishMessageWrapper(messages[0], None))
        batch.publish(PublishMessageWrapper(messages[1], None))

    # The server side limit should kick in and cause a commit.
    fake_commit.assert_called_once()


def test_publish_dict():
    batch = create_batch()
    message = PublishMessageWrapper(
        gapic_types.PubsubMessage(data=b"foobarbaz", attributes={"spam": "eggs"}), None
    )
    future = batch.publish(message)

    # There should be one message on the batch.
    expected_message = PublishMessageWrapper(
        gapic_types.PubsubMessage(data=b"foobarbaz", attributes={"spam": "eggs"}), None
    )
    assert batch.message_wrappers == [expected_message]
    assert batch._futures == [future]


def test_cancel():
    batch = create_batch()
    futures = (
        batch.publish(
            PublishMessageWrapper(
                gapic_types.PubsubMessage(data=b"This is my message."), None
            )
        ),
        batch.publish(
            PublishMessageWrapper(
                gapic_types.PubsubMessage(data=b"This is another message."), None
            )
        ),
    )

    batch.cancel(BatchCancellationReason.PRIOR_ORDERED_MESSAGE_FAILED)

    # Assert all futures are cancelled with an error.
    for future in futures:
        exc = future.exception()
        assert type(exc) is RuntimeError
        assert exc.args[0] == BatchCancellationReason.PRIOR_ORDERED_MESSAGE_FAILED.value


def test_do_not_commit_when_full_when_flag_is_off():
    max_messages = 4
    # Set commit_when_full flag to False
    batch = create_batch(max_messages=max_messages, commit_when_full=False)
    messages = (
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None),
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"spameggs"), None),
        PublishMessageWrapper(gapic_types.PubsubMessage(data=b"1335020400"), None),
    )

    with mock.patch.object(batch, "commit") as commit:
        # Publish 3 messages.
        futures = [batch.publish(message) for message in messages]
        assert len(futures) == 3

        # When a fourth message is published, commit should not be called.
        future = batch.publish(
            PublishMessageWrapper(gapic_types.PubsubMessage(data=b"last one"), None)
        )
        assert commit.call_count == 0
        assert future is None


class BatchDoneCallbackTracker(object):
    def __init__(self):
        self.called = False
        self.success = None

    def __call__(self, success):
        self.called = True
        self.success = success


# Refer https://opentelemetry.io/docs/languages/python/#version-support
@pytest.mark.skipif(
    sys.version_info < (3, 8), reason="Open Telemetry requires python3.8 or higher"
)
def test_commit_otel_publish_rpc_span_exception(span_exporter):
    TOPIC = "projects/projectID/topics/topicID"
    batch = create_batch(topic=TOPIC, enable_open_telemetry=True)

    tracer = trace.get_tracer_provider().get_tracer("com.google.cloud.pubsub.v1")
    with tracer.start_as_current_span(name="foo", end_on_exit=False) as create_span:
        message = PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"foo"), span=create_span
        )
    batch.publish(message)

    # Mock publish error.
    error = google.api_core.exceptions.InternalServerError("error")

    with mock.patch.object(
        type(batch.client),
        "_gapic_publish",
        side_effect=error,
    ):
        batch._commit()

    spans = span_exporter.get_finished_spans()
    # Span 1: publish RPC Span
    # Span 2: create span of message.
    assert len(spans) == 2

    # Verify status of both spans recorded error and exception event.
    for span in spans:
        assert span.status.status_code == trace.status.StatusCode.ERROR
        assert len(span.events) == 1
        assert span.events[0].name == "exception"
        assert span.end_time is not None


def test_commit_otel_null_span(span_exporter):
    """
    Test case checks the null case check scenario and appeases code coverage.
    This scenario where open telemetry is enabled, yet the message added to the
    batch does not contain a span should not arise in the library.
    """
    TOPIC = "projects/projectID/topics/topic"
    batch = create_batch(
        topic=TOPIC,
        enable_open_telemetry=True,
    )

    msg = PublishMessageWrapper(
        message=gapic_types.PubsubMessage(data=b"foo"),
    )

    batch.publish(msg)

    publish_response = gapic_types.PublishResponse(message_ids=["a"])
    with mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    ):
        batch._commit()

    spans = span_exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == f"{TOPIC} publish"
    assert spans[0].end_time is not None

    error = google.api_core.exceptions.InternalServerError("error")
    batch = create_batch(
        topic=TOPIC,
        enable_open_telemetry=True,
    )
    batch.publish(msg)

    with mock.patch.object(
        type(batch.client),
        "_gapic_publish",
        side_effect=error,
    ):
        batch._commit()

    assert len(spans) == 1
    assert spans[0].name == f"{TOPIC} publish"
    assert spans[0].end_time is not None


def test_commit_otel_publish_non_sampled(span_exporter):
    TOPIC = "projects/projectID/topics/topic"
    batch = create_batch(
        topic=TOPIC,
        enable_open_telemetry=True,
    )

    tracer = trace.get_tracer_provider().get_tracer("com.google.cloud.pubsub.v1")
    with tracer.start_as_current_span(name="foo", end_on_exit=False) as span:
        span.is_recording = mock.Mock(return_value=False)
        msg = PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"foo"), span=span
        )

    batch.publish(msg)

    publish_response = gapic_types.PublishResponse(message_ids=["a"])
    with mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    ):
        batch._commit()

    spans = span_exporter.get_finished_spans()

    # Span 1: publish RPC Span
    # Span 2: create span of message.
    assert len(spans) == 2
    publish_rpc_span, create_span = spans
    assert len(publish_rpc_span.links) == 0
    assert len(create_span.links) == 0


@pytest.mark.skipif(
    sys.version_info < (3, 8), reason="Open Telemetry requires python3.8 or higher"
)
def test_commit_otel_publish_rpc_span(span_exporter):
    TOPIC = "projects/projectID/topics/topic"
    batch = create_batch(
        topic=TOPIC,
        enable_open_telemetry=True,
    )

    # Simulate message 1 published with its own publisher create span.
    tracer = trace.get_tracer_provider().get_tracer("com.google.cloud.pubsub.v1")
    with tracer.start_as_current_span(name="foo", end_on_exit=False) as create_span1:
        msg1 = PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"foo"), span=create_span1
        )

    # Simulate message 2 published with its own publisher create span.
    with tracer.start_as_current_span(name="bar", end_on_exit=False) as create_span2:
        msg2 = PublishMessageWrapper(
            message=gapic_types.PubsubMessage(data=b"bar"),
            span=create_span2,
        )

    # Add both messages to the batch.
    batch.publish(msg1)
    batch.publish(msg2)

    publish_response = gapic_types.PublishResponse(message_ids=["a", "b"])
    with mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    ):
        batch._commit()

    spans = span_exporter.get_finished_spans()

    # Span 1: publish RPC span - closed after publish RPC success.
    # Span 2: publisher create span of message 1 - closed after publish RPC success.
    # Span 3: publisher create span of message 2 - closed after publish RPC success.
    assert len(spans) == 3
    # publish_rpc_span, create_span_1, create_span2, non_sampled_span = spans
    publish_rpc_span, create_span_1, create_span2 = spans

    # Verify publish_rpc_span
    assert publish_rpc_span.name == f"{TOPIC} publish"
    assert publish_rpc_span.kind == trace.SpanKind.CLIENT
    assert publish_rpc_span.end_time is not None
    attributes = publish_rpc_span.attributes
    assert attributes["messaging.system"] == "com.google.cloud.pubsub.v1"
    assert attributes["messaging.destination.name"] == TOPIC
    assert attributes["gcp.project_id"] == "projectID"
    assert attributes["messaging.batch.message_count"] == 2
    assert attributes["messaging.operation"] == "publish"
    assert attributes["code.function"] == "_commit"
    assert publish_rpc_span.parent is None
    # Verify the links correspond to the spans of the published messages.
    assert len(publish_rpc_span.links) == 2
    assert publish_rpc_span.links[0].context[1] == create_span_1.context[1]
    assert publish_rpc_span.links[1].context[1] == create_span2.context[1]

    # Verify spans of the published messages.
    assert create_span_1.name == "foo"
    assert create_span2.name == "bar"

    # Verify the publish create spans have been closed after publish success.
    assert create_span1.end_time is not None
    assert create_span2.end_time is not None

    # Verify message_ids returned from gapic publish are added as attributes
    # to the publisher create spans of the messages.
    assert "messaging.message.id" in create_span1.attributes
    assert create_span1.attributes["messaging.message.id"] == "a"
    assert "messaging.message.id" in create_span2.attributes
    assert create_span2.attributes["messaging.message.id"] == "b"

    # Verify publish end event added to the span
    assert len(create_span1.events) == 1
    assert len(create_span2.events) == 1
    assert create_span1.events[0].name == "publish end"
    assert create_span2.events[0].name == "publish end"


def test_batch_done_callback_called_on_success():
    batch_done_callback_tracker = BatchDoneCallbackTracker()
    batch = create_batch(batch_done_callback=batch_done_callback_tracker)

    # Ensure messages exist.
    message = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    batch.publish(message)

    # One response for one published message.
    publish_response = gapic_types.PublishResponse(message_ids=["a"])

    with mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    ):
        batch._commit()

    assert batch_done_callback_tracker.called
    assert batch_done_callback_tracker.success


def test_batch_done_callback_called_on_publish_failure():
    batch_done_callback_tracker = BatchDoneCallbackTracker()
    batch = create_batch(batch_done_callback=batch_done_callback_tracker)

    # Ensure messages exist.
    message = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    batch.publish(message)

    # One response for one published message.
    publish_response = gapic_types.PublishResponse(message_ids=["a"])

    # Induce publish error.
    error = google.api_core.exceptions.InternalServerError("uh oh")

    with mock.patch.object(
        type(batch.client),
        "_gapic_publish",
        return_value=publish_response,
        side_effect=error,
    ):
        batch._commit()

    assert batch_done_callback_tracker.called
    assert not batch_done_callback_tracker.success


def test_batch_done_callback_called_on_publish_response_invalid():
    batch_done_callback_tracker = BatchDoneCallbackTracker()
    batch = create_batch(batch_done_callback=batch_done_callback_tracker)

    # Ensure messages exist.
    message = PublishMessageWrapper(gapic_types.PubsubMessage(data=b"foobarbaz"), None)
    batch.publish(message)

    # No message ids returned in successful publish response -> invalid.
    publish_response = gapic_types.PublishResponse(message_ids=[])

    with mock.patch.object(
        type(batch.client), "_gapic_publish", return_value=publish_response
    ):
        batch._commit()

    assert batch_done_callback_tracker.called
    assert not batch_done_callback_tracker.success
