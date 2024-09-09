# Copyright 2020, Google LLC
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
import logging
from typing import Any, Callable, Iterable, Optional

from google.cloud.pubsub_v1.open_telemetry.subscribe_message_wrapper import (
    SubscribeMessageWrapper,
)

_LOGGER = logging.getLogger(__name__)


class MessagesOnHold(object):
    """Tracks messages on hold by ordering key. Not thread-safe."""

    def __init__(self):
        self._size = 0

        # A FIFO queue for the messages that have been received from the server,
        # but not yet sent to the user callback.
        # Both ordered and unordered messages may be in this queue. Ordered
        # message state tracked in _pending_ordered_messages once ordered
        # messages are taken off this queue.
        # The tail of the queue is to the right side of the deque; the head is
        # to the left side.
        self._messages_on_hold = collections.deque()

        # Dict of ordering_key -> queue of ordered messages that have not been
        # delivered to the user.
        # All ordering keys in this collection have a message in flight. Once
        # that one is acked or nacked, the next message in the queue for that
        # ordering key will be sent.
        # If the queue is empty, it means there's a message for that key in
        # flight, but there are no pending messages.
        self._pending_ordered_messages = {}

    @property
    def size(self) -> int:
        """Return the number of messages on hold across ordered and unordered messages.

        Note that this object may still store information about ordered messages
        in flight even if size is zero.

        Returns:
            The size value.
        """
        return self._size

    def get(self) -> Optional[SubscribeMessageWrapper]:
        """Gets a message wrapper from the on-hold queue. A message with an ordering
        key won't be returned if there's another message with the same key in
        flight.

        Returns:
            A message wrapper that hasn't been sent to the user yet or ``None`` if there are no
            message wrappers available.
        """
        while self._messages_on_hold:
            wrapper = self._messages_on_hold.popleft()
            msg = wrapper.subscriber_message

            if msg.ordering_key:
                pending_queue = self._pending_ordered_messages.get(msg.ordering_key)
                if pending_queue is None:
                    # Create empty queue to indicate a message with the
                    # ordering key is in flight.
                    self._pending_ordered_messages[
                        msg.ordering_key
                    ] = collections.deque()
                    self._size = self._size - 1
                    return wrapper
                else:
                    # Another message is in flight so add message to end of
                    # queue for this ordering key.
                    pending_queue.append(wrapper)
            else:
                # Unordered messages can be returned without any
                # restrictions.
                self._size = self._size - 1
                return wrapper

        return None

    def put(self, wrapper: SubscribeMessageWrapper) -> None:
        """Put a message wrapper on hold.

        Args:
            wrapper: The message wrapper to put on hold.
        """
        self._messages_on_hold.append(wrapper)
        self._size = self._size + 1

    def activate_ordering_keys(
        self,
        ordering_keys: Iterable[str],
        schedule_message_callback: Callable[[SubscribeMessageWrapper], Any],
    ) -> None:
        """Send the next message in the queue for each of the passed-in
        ordering keys, if they exist. Clean up state for keys that no longer
        have any queued messages.

        See comment at streaming_pull_manager.activate_ordering_keys() for more
        detail about the impact of this method on load.

        Args:
            ordering_keys:
                The ordering keys to activate. May be empty, or contain duplicates.
            schedule_message_callback:
                The callback to call to schedule a message to be sent to the user.
        """
        for key in ordering_keys:
            pending_ordered_wrappers = self._pending_ordered_messages.get(key)
            if pending_ordered_wrappers is None:
                _LOGGER.warning(
                    "No message queue exists for message ordering key: %s.", key
                )
                continue
            next_wrapper = self._get_next_for_ordering_key(key)
            if next_wrapper:
                # Schedule the next message because the previous was dropped.
                # Note that this may overload the user's `max_bytes` limit, but
                # not their `max_messages` limit.
                schedule_message_callback(next_wrapper)
            else:
                # No more messages for this ordering key, so do clean-up.
                self._clean_up_ordering_key(key)

    def _get_next_for_ordering_key(
        self, ordering_key: str
    ) -> Optional[SubscribeMessageWrapper]:
        """Get next message for ordering key.

        The client should call clean_up_ordering_key() if this method returns
        None.

        Args:
            ordering_key: Ordering key for which to get the next message.

        Returns:
            The next message wrapper for this ordering key or None if there aren't any.
        """
        wrapper_queue_for_key = self._pending_ordered_messages.get(ordering_key)
        if wrapper_queue_for_key:
            self._size = self._size - 1
            return wrapper_queue_for_key.popleft()
        return None

    def _clean_up_ordering_key(self, ordering_key: str) -> None:
        """Clean up state for an ordering key with no pending messages.

        Args
            ordering_key: The ordering key to clean up.
        """
        wrapper_queue = self._pending_ordered_messages.get(ordering_key)
        if wrapper_queue is None:
            _LOGGER.warning(
                "Tried to clean up ordering key that does not exist: %s", ordering_key
            )
            return
        if len(wrapper_queue) > 0:
            _LOGGER.warning(
                "Tried to clean up ordering key: %s with %d messages remaining.",
                ordering_key,
                len(wrapper_queue),
            )
            return
        del self._pending_ordered_messages[ordering_key]
