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

import concurrent.futures
import threading
import time

import mock
import pytest
import warnings

from google.cloud.pubsub_v1 import exceptions
from google.cloud.pubsub_v1 import futures


def _future(*args, **kwargs):
    return futures.Future(*args, **kwargs)


def test_constructor_default_no_warning():
    with warnings.catch_warnings(record=True) as warned:
        _future()
    assert not warned


def test_constructor_custom_completed_arg():
    completed = mock.sentinel.completed

    with warnings.catch_warnings(record=True) as warned:
        _future(completed=completed)

    assert len(warned) == 1
    assert issubclass(warned[0].category, DeprecationWarning)
    warning_msg = str(warned[0].message)
    assert "completed" in warning_msg
    assert "not used" in warning_msg


def test_running():
    future = _future()
    assert future.running() is True
    future.set_result("foobar")
    assert future.running() is False


def test_done():
    future = _future()
    assert future.done() is False
    future.set_result("12345")
    assert future.done() is True


def test_exception_no_error():
    future = _future()
    future.set_result("12345")
    assert future.exception() is None


def test_exception_with_error():
    future = _future()
    error = RuntimeError("Something really bad happened.")
    future.set_exception(error)

    # Make sure that the exception that is returned is the batch's error.
    # Also check the type to ensure the batch's error did not somehow
    # change internally.
    assert future.exception() is error
    assert isinstance(future.exception(), RuntimeError)
    with pytest.raises(RuntimeError):
        future.result()


def test_exception_timeout():
    future = _future()
    with pytest.raises(exceptions.TimeoutError):
        future.exception(timeout=0.01)


def test_result_no_error():
    future = _future()
    future.set_result("42")
    assert future.result() == "42"


def test_result_with_error():
    future = _future()
    future.set_exception(RuntimeError("Something really bad happened."))
    with pytest.raises(RuntimeError):
        future.result()


def test_add_done_callback_pending_batch():
    future = _future()
    callback = mock.Mock()
    future.add_done_callback(callback)
    assert len(future._done_callbacks) == 1
    assert callback in future._done_callbacks
    assert callback.call_count == 0


def test_add_done_callback_completed_batch():
    future = _future()
    future.set_result("12345")
    callback = mock.Mock(spec=())
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


def test_trigger():
    future = _future()
    callback = mock.Mock(spec=())
    future.add_done_callback(callback)
    assert callback.call_count == 0
    future.set_result("12345")
    callback.assert_called_once_with(future)


def test_set_result_once_only():
    future = _future()
    future.set_result("12345")
    with pytest.raises(concurrent.futures.InvalidStateError):
        future.set_result("67890")


def test_set_exception_once_only():
    future = _future()
    future.set_exception(ValueError("wah wah"))
    with pytest.raises(concurrent.futures.InvalidStateError):
        future.set_exception(TypeError("other wah wah"))


def test_as_completed_compatibility():
    all_futures = {i: _future() for i in range(6)}
    done_futures = []

    def resolve_future(future_idx, delay=0):
        time.sleep(delay)
        future = all_futures[future_idx]
        if future_idx % 2 == 0:
            future.set_result(f"{future_idx}: I'm done!")
        else:
            future.set_exception(Exception(f"Future {future_idx} errored"))

    all_futures[2].set_result("2: I'm done!")

    # Start marking the futures as completed (either with success or error) at
    # different times and check that ther "as completed" order is correct.
    for future_idx, delay in ((0, 0.8), (3, 0.6), (1, 0.4), (5, 0.2)):
        threading.Thread(
            target=resolve_future, args=(future_idx, delay), daemon=True
        ).start()

    try:
        # Use a loop instead of a list comprehension to gather futures completed
        # before the timeout error occurs.
        for future in concurrent.futures.as_completed(all_futures.values(), timeout=1):
            done_futures.append(future)
    except concurrent.futures.TimeoutError:
        pass
    else:  # pragma: NO COVER
        pytest.fail("Not all Futures should have been recognized as completed.")

    # NOTE: Future 4 was never resolved.
    expected = [
        all_futures[2],
        all_futures[5],
        all_futures[1],
        all_futures[3],
        all_futures[0],
    ]
    assert done_futures == expected
