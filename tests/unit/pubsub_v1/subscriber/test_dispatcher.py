# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import queue
import threading

from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber._protocol import requests
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager
from google.pubsub_v1 import types as gapic_types

import mock
import pytest


@pytest.mark.parametrize(
    "item,method_name",
    [
        (requests.AckRequest("0", 0, 0, "", None), "ack"),
        (requests.DropRequest("0", 0, ""), "drop"),
        (requests.LeaseRequest("0", 0, ""), "lease"),
        (requests.ModAckRequest("0", 0, None), "modify_ack_deadline"),
        (requests.NackRequest("0", 0, "", None), "nack"),
    ],
)
def test_dispatch_callback_active_manager(item, method_name):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [item]

    with mock.patch.object(dispatcher_, method_name) as method:
        dispatcher_.dispatch_callback(items)

    method.assert_called_once_with([item])


@pytest.mark.parametrize(
    "item,method_name",
    [
        (requests.AckRequest("0", 0, 0, "", None), "ack"),
        (requests.DropRequest("0", 0, ""), "drop"),
        (requests.LeaseRequest("0", 0, ""), "lease"),
        (requests.ModAckRequest("0", 0, None), "modify_ack_deadline"),
        (requests.NackRequest("0", 0, "", None), "nack"),
    ],
)
def test_dispatch_callback_inactive_manager(item, method_name):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    manager.is_active = False
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [item]

    with mock.patch.object(dispatcher_, method_name) as method:
        dispatcher_.dispatch_callback(items)

    method.assert_called_once_with([item])


def test_ack():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.AckRequest(
            ack_id="ack_id_string", byte_size=0, time_to_ack=20, ordering_key="",
            future=None
        )
    ]
    manager.send_unary_ack.return_value = (items, [])
    dispatcher_.ack(items)

    manager.send_unary_ack.assert_called_once_with(ack_ids=["ack_id_string"], future_reqs_dict={})

    manager.leaser.remove.assert_called_once_with(items)
    manager.maybe_resume_consumer.assert_called_once()
    manager.ack_histogram.add.assert_called_once_with(20)


def test_ack_no_time():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.AckRequest(
            ack_id="ack_id_string", byte_size=0, time_to_ack=None, ordering_key="",
            future=None
        )
    ]
    manager.send_unary_ack.return_value = (items, [])
    dispatcher_.ack(items)

    manager.send_unary_ack.assert_called_once_with(ack_ids=["ack_id_string"], future_reqs_dict={})

    manager.ack_histogram.add.assert_not_called()


def test_ack_splitting_large_payload():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        # use realistic lengths for ACK IDs (max 176 bytes)
        requests.AckRequest(
            ack_id=str(i).zfill(176), byte_size=0, time_to_ack=20, ordering_key="",
            future=None
        )
        for i in range(5001)
    ]
    manager.send_unary_ack.return_value = (items, [])
    dispatcher_.ack(items)

    calls = manager.send_unary_ack.call_args_list
    assert len(calls) == 3

    all_ack_ids = {item.ack_id for item in items}
    sent_ack_ids = collections.Counter()

    for call in calls:
        ack_ids = call[1]["ack_ids"]
        assert len(ack_ids) <= dispatcher._ACK_IDS_BATCH_SIZE
        sent_ack_ids.update(ack_ids)

    assert set(sent_ack_ids) == all_ack_ids  # all messages should have been ACK-ed
    assert sent_ack_ids.most_common(1)[0][1] == 1  # each message ACK-ed exactly once


def test_lease():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.LeaseRequest(ack_id="ack_id_string", byte_size=10, ordering_key="")
    ]
    dispatcher_.lease(items)

    manager.leaser.add.assert_called_once_with(items)
    manager.maybe_pause_consumer.assert_called_once()


def test_drop_unordered_messages():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.DropRequest(ack_id="ack_id_string", byte_size=10, ordering_key="")
    ]
    dispatcher_.drop(items)

    manager.leaser.remove.assert_called_once_with(items)
    assert list(manager.activate_ordering_keys.call_args.args[0]) == []
    manager.maybe_resume_consumer.assert_called_once()


def test_drop_ordered_messages():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.DropRequest(ack_id="ack_id_string", byte_size=10, ordering_key=""),
        requests.DropRequest(ack_id="ack_id_string", byte_size=10, ordering_key="key1"),
        requests.DropRequest(ack_id="ack_id_string", byte_size=10, ordering_key="key2"),
    ]
    dispatcher_.drop(items)

    manager.leaser.remove.assert_called_once_with(items)
    assert list(manager.activate_ordering_keys.call_args.args[0]) == ["key1", "key2"]
    manager.maybe_resume_consumer.assert_called_once()


def test_nack():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        requests.NackRequest(ack_id="ack_id_string", byte_size=10, ordering_key="", future=None)
    ]
    manager.send_unary_modack.return_value = (items, [])
    dispatcher_.nack(items)

    manager.send_unary_modack.assert_called_once_with(
        modify_deadline_ack_ids=["ack_id_string"], modify_deadline_seconds=[0], future_reqs_dict={}
    )


def test_modify_ack_deadline():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [requests.ModAckRequest(ack_id="ack_id_string", seconds=60, future=None)]
    manager.send_unary_modack.return_value = (items, [])
    dispatcher_.modify_ack_deadline(items)

    manager.send_unary_modack.assert_called_once_with(
        modify_deadline_ack_ids=["ack_id_string"], modify_deadline_seconds=[60], future_reqs_dict={}
    )


def test_modify_ack_deadline_splitting_large_payload():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    items = [
        # use realistic lengths for ACK IDs (max 176 bytes)
        requests.ModAckRequest(ack_id=str(i).zfill(176), seconds=60, future=None)
        for i in range(5001)
    ]
    manager.send_unary_modack.return_value = (items, [])
    dispatcher_.modify_ack_deadline(items)

    calls = manager.send_unary_modack.call_args_list
    assert len(calls) == 3

    all_ack_ids = {item.ack_id for item in items}
    sent_ack_ids = collections.Counter()

    for call in calls:
        modack_ackids = call[1]["modify_deadline_ack_ids"]
        print(type(modack_ackids))
        assert len(modack_ackids) <= dispatcher._ACK_IDS_BATCH_SIZE
        sent_ack_ids.update(modack_ackids)

    assert set(sent_ack_ids) == all_ack_ids  # all messages should have been MODACK-ed
    assert sent_ack_ids.most_common(1)[0][1] == 1  # each message MODACK-ed exactly once


@mock.patch("threading.Thread", autospec=True)
def test_start(thread):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)

    dispatcher_.start()

    thread.assert_called_once_with(
        name=dispatcher._CALLBACK_WORKER_NAME, target=mock.ANY
    )

    thread.return_value.start.assert_called_once()

    assert dispatcher_._thread is not None


@mock.patch("threading.Thread", autospec=True)
def test_start_already_started(thread):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True
    )
    dispatcher_ = dispatcher.Dispatcher(manager, mock.sentinel.queue)
    dispatcher_._thread = mock.sentinel.thread

    with pytest.raises(ValueError):
        dispatcher_.start()

    thread.assert_not_called()


def test_stop():
    queue_ = queue.Queue()
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.manager, queue_)
    thread = mock.create_autospec(threading.Thread, instance=True)
    dispatcher_._thread = thread

    dispatcher_.stop()

    assert queue_.get() is helper_threads.STOP
    thread.join.assert_called_once()
    assert dispatcher_._thread is None


def test_stop_no_join():
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.manager, mock.sentinel.queue)

    dispatcher_.stop()
