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

import logging
import threading
import warnings

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions


_LOGGER = logging.getLogger(__name__)


class FlowController(object):
    """A class used to control the flow of messages passing through it.

    Args:
        settings (~google.cloud.pubsub_v1.types.PublishFlowControl):
            Desired flow control configuration.
    """

    def __init__(self, settings):
        self._settings = settings

        self._message_count = 0
        self._total_bytes = 0

        # The lock is used to protect the internal state (message and byte count).
        self._operational_lock = threading.Lock()

        # The condition for blocking the flow if capacity is exceeded.
        self._has_capacity = threading.Condition(lock=self._operational_lock)

    def add(self, message):
        """Add a message to flow control.

        Adding a message updates the internal load statistics, and an action is
        taken if these limits are exceeded (depending on the flow control settings).

        Args:
            message (:class:`~google.cloud.pubsub_v1.types.PubsubMessage`):
                The message entering the flow control.

        Raises:
            :exception:`~pubsub_v1.publisher.exceptions.FlowControlLimitError`:
                If adding a message exceeds flow control limits and the desired
                action is :attr:`~google.cloud.pubsub_v1.types.LimitExceededBehavior.ERROR`.
        """
        if self._settings.limit_exceeded_behavior == types.LimitExceededBehavior.IGNORE:
            return

        with self._operational_lock:
            self._message_count += 1
            self._total_bytes += message.ByteSize()

            if not self._is_overflow():
                return

            # We have an overflow, react.
            if (
                self._settings.limit_exceeded_behavior
                == types.LimitExceededBehavior.ERROR
            ):
                msg = (
                    "Flow control limits exceeded "
                    "(messages: {} / {}, bytes: {} / {})."
                ).format(
                    self._message_count,
                    self._settings.message_limit,
                    self._total_bytes,
                    self._settings.byte_limit,
                )
                error = exceptions.FlowControlLimitError(msg)

                # Raising an error means rejecting a message, thus we need to deduct
                # the latter's contribution to the total load.
                self._message_count -= 1
                self._total_bytes -= message.ByteSize()
                raise error

            assert (
                self._settings.limit_exceeded_behavior
                == types.LimitExceededBehavior.BLOCK
            )

            while self._is_overflow():
                _LOGGER.debug(
                    "Blocking until there is enough free capacity in the flow."
                )
                self._has_capacity.wait()
                _LOGGER.debug("Woke up from waiting on free capacity in the flow.")

    def release(self, message):
        """Release a mesage from flow control.

        Args:
            message (:class:`~google.cloud.pubsub_v1.types.PubsubMessage`):
                The message entering the flow control.
        """
        if self._settings.limit_exceeded_behavior == types.LimitExceededBehavior.IGNORE:
            return

        with self._operational_lock:
            was_overflow = self._is_overflow()

            self._message_count -= 1
            self._total_bytes -= message.ByteSize()

            if self._message_count < 0 or self._total_bytes < 0:
                warnings.warn(
                    "Releasing a message that was never added or already released.",
                    category=RuntimeWarning,
                    stacklevel=2,
                )
                self._message_count = max(0, self._message_count)
                self._total_bytes = max(0, self._total_bytes)

            if was_overflow and not self._is_overflow():
                _LOGGER.debug("Notifying threads waiting to add messages to flow.")
                self._has_capacity.notify_all()

    def _is_overflow(self):
        """Determine if the current message load exceeds flow control limits.

        The method assumes that the caller has obtained ``_operational_lock``.

        Returns:
            bool
        """
        return (
            self._message_count > self._settings.message_limit
            or self._total_bytes > self._settings.byte_limit
        )
