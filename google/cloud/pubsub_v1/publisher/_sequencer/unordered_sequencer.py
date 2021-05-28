# Copyright 2019, Google LLC All rights reserved.
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

from google.api_core import gapic_v1

from google.cloud.pubsub_v1.publisher._sequencer import base
from google.pubsub_v1 import types as gapic_types


class UnorderedSequencer(base.Sequencer):
    """ Sequences messages into batches for one topic without any ordering.

        Public methods are NOT thread-safe.
    """

    def __init__(self, client, topic):
        self._client = client
        self._topic = topic
        self._current_batch = None
        self._stopped = False

    def is_finished(self):
        """ Whether the sequencer is finished and should be cleaned up.

            Returns:
                bool: Whether the sequencer is finished and should be cleaned up.
        """
        # TODO: Implement. Not implementing yet because of possible performance
        # impact due to extra locking required. This does mean that
        # UnorderedSequencers don't get cleaned up, but this is the same as
        # previously existing behavior.
        return False

    def stop(self):
        """ Stop the sequencer.

            Subsequent publishes will fail.

            Raises:
                RuntimeError:
                    If called after stop() has already been called.
        """
        if self._stopped:
            raise RuntimeError("Unordered sequencer already stopped.")
        self.commit()
        self._stopped = True

    def commit(self):
        """ Commit the batch.

            Raises:
                RuntimeError:
                    If called after stop() has already been called.
        """
        if self._stopped:
            raise RuntimeError("Unordered sequencer already stopped.")
        if self._current_batch:
            self._current_batch.commit()

            # At this point, we lose track of the old batch, but we don't
            # care since we just committed it.
            # Setting this to None guarantees the next publish() creates a new
            # batch.
            self._current_batch = None

    def unpause(self):
        """ Not relevant for this class. """
        raise NotImplementedError

    def _create_batch(
        self,
        commit_retry=gapic_v1.method.DEFAULT,
        commit_timeout: gapic_types.TimeoutType = gapic_v1.method.DEFAULT,
    ):
        """ Create a new batch using the client's batch class and other stored
            settings.

        Args:
            commit_retry (Optional[google.api_core.retry.Retry]):
                The retry settings to apply when publishing the batch.
            commit_timeout (:class:`~.pubsub_v1.types.TimeoutType`):
                The timeout to apply when publishing the batch.
        """
        return self._client._batch_class(
            client=self._client,
            topic=self._topic,
            settings=self._client.batch_settings,
            batch_done_callback=None,
            commit_when_full=True,
            commit_retry=commit_retry,
            commit_timeout=commit_timeout,
        )

    def publish(
        self,
        message,
        retry=gapic_v1.method.DEFAULT,
        timeout: gapic_types.TimeoutType = gapic_v1.method.DEFAULT,
    ):
        """ Batch message into existing or new batch.

        Args:
            message (~.pubsub_v1.types.PubsubMessage):
                The Pub/Sub message.
            retry (Optional[google.api_core.retry.Retry]):
                The retry settings to apply when publishing the message.
            timeout (:class:`~.pubsub_v1.types.TimeoutType`):
                The timeout to apply when publishing the message.

        Returns:
            ~google.api_core.future.Future: An object conforming to
            the :class:`~concurrent.futures.Future` interface. The future tracks
            the publishing status of the message.

        Raises:
            RuntimeError:
                If called after stop() has already been called.

            pubsub_v1.publisher.exceptions.MessageTooLargeError: If publishing
                the ``message`` would exceed the max size limit on the backend.
        """
        if self._stopped:
            raise RuntimeError("Unordered sequencer already stopped.")

        if not self._current_batch:
            newbatch = self._create_batch(commit_retry=retry, commit_timeout=timeout)
            self._current_batch = newbatch

        batch = self._current_batch
        future = None
        while future is None:
            # Might throw MessageTooLargeError
            future = batch.publish(message)
            # batch is full, triggering commit_when_full
            if future is None:
                batch = self._create_batch(commit_retry=retry, commit_timeout=timeout)
                # At this point, we lose track of the old batch, but we don't
                # care since it's already committed (because it was full.)
                self._current_batch = batch
        return future

    # Used only for testing.
    def _set_batch(self, batch):
        self._current_batch = batch
