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

from __future__ import absolute_import

import os
import pkg_resources
import typing
from typing import Any, Callable, Optional, Sequence, Union

from google.auth.credentials import AnonymousCredentials
from google.oauth2 import service_account

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import futures
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager
from google.pubsub_v1.services.subscriber import client as subscriber_client

if typing.TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.pubsub_v1 import subscriber


try:
    __version__ = pkg_resources.get_distribution("google-cloud-pubsub").version
except pkg_resources.DistributionNotFound:
    # Distribution might not be available if we are not running from within
    # a PIP package.
    __version__ = "0.0"

_DENYLISTED_METHODS = (
    "publish",
    "from_service_account_file",
    "from_service_account_json",
)


@_gapic.add_methods(subscriber_client.SubscriberClient, denylist=_DENYLISTED_METHODS)
class Client(object):
    """A subscriber client for Google Cloud Pub/Sub.

    This creates an object that is capable of subscribing to messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        kwargs: Any additional arguments provided are sent as keyword
            keyword arguments to the underlying
            :class:`~google.cloud.pubsub_v1.gapic.subscriber_client.SubscriberClient`.
            Generally you should not need to set additional keyword
            arguments. Optionally, regional endpoints can be set via
            ``client_options`` that takes a single key-value pair that
            defines the endpoint.

    Example:

    .. code-block:: python

        from google.cloud import pubsub_v1

        subscriber_client = pubsub_v1.SubscriberClient(
            # Optional
            client_options = {
                "api_endpoint": REGIONAL_ENDPOINT
            }
        )
    """

    def __init__(self, **kwargs: Any):
        # Sanity check: Is our goal to use the emulator?
        # If so, create a grpc insecure channel with the emulator host
        # as the target.
        if os.environ.get("PUBSUB_EMULATOR_HOST"):
            kwargs["client_options"] = {
                "api_endpoint": os.environ.get("PUBSUB_EMULATOR_HOST")
            }
            kwargs["credentials"] = AnonymousCredentials()

        # Instantiate the underlying GAPIC client.
        self._api = subscriber_client.SubscriberClient(**kwargs)
        self._target = self._api._transport._host
        self._closed = False

    @classmethod
    def from_service_account_file(cls, filename: str, **kwargs: Any) -> "Client":
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename: The path to the service account private key json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            A Subscriber :class:`~google.cloud.pubsub_v1.subscriber.client.Client`
            instance that is the constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(**kwargs)

    from_service_account_json = from_service_account_file

    @property
    def target(self) -> str:
        """Return the target (where the API is).

        Returns:
            The location of the API.
        """
        return self._target

    @property
    def api(self) -> subscriber_client.SubscriberClient:
        """The underlying gapic API client."""
        return self._api

    @property
    def closed(self) -> bool:
        """Return whether the client has been closed and cannot be used anymore.

        .. versionadded:: 2.8.0
        """
        return self._closed

    def subscribe(
        self,
        subscription: str,
        callback: Callable[["subscriber.message.Message"], Any],
        flow_control: Union[types.FlowControl, Sequence] = (),
        scheduler: Optional["subscriber.scheduler.Scheduler"] = None,
        use_legacy_flow_control: bool = False,
        await_callbacks_on_shutdown: bool = False,
    ) -> futures.StreamingPullFuture:
        """Asynchronously start receiving messages on a given subscription.

        This method starts a background thread to begin pulling messages from
        a Pub/Sub subscription and scheduling them to be processed using the
        provided ``callback``.

        The ``callback`` will be called with an individual
        :class:`google.cloud.pubsub_v1.subscriber.message.Message`. It is the
        responsibility of the callback to either call ``ack()`` or ``nack()``
        on the message when it finished processing. If an exception occurs in
        the callback during processing, the exception is logged and the message
        is ``nack()`` ed.

        The ``flow_control`` argument can be used to control the rate of at
        which messages are pulled. The settings are relatively conservative by
        default to prevent "message hoarding" - a situation where the client
        pulls a large number of messages but can not process them fast enough
        leading it to "starve" other clients of messages. Increasing these
        settings may lead to faster throughput for messages that do not take
        a long time to process.

        The ``use_legacy_flow_control`` argument disables enforcing flow control
        settings at the Cloud Pub/Sub server, and only the client side flow control
        will be enforced.

        This method starts the receiver in the background and returns a
        *Future* representing its execution. Waiting on the future (calling
        ``result()``) will block forever or until a non-recoverable error
        is encountered (such as loss of network connectivity). Cancelling the
        future will signal the process to shutdown gracefully and exit.

        .. note:: This uses Pub/Sub's *streaming pull* feature. This feature
            properties that may be surprising. Please take a look at
            https://cloud.google.com/pubsub/docs/pull#streamingpull for
            more details on how streaming pull behaves compared to the
            synchronous pull method.

        Example:

        .. code-block:: python

            from google.cloud import pubsub_v1

            subscriber_client = pubsub_v1.SubscriberClient()

            # existing subscription
            subscription = subscriber_client.subscription_path(
                'my-project-id', 'my-subscription')

            def callback(message):
                print(message)
                message.ack()

            future = subscriber_client.subscribe(
                subscription, callback)

            try:
                future.result()
            except KeyboardInterrupt:
                future.cancel()  # Trigger the shutdown.
                future.result()  # Block until the shutdown is complete.

        Args:
            subscription:
                The name of the subscription. The subscription should have already been
                created (for example, by using :meth:`create_subscription`).
            callback:
                The callback function. This function receives the message as
                its only argument and will be called from a different thread/
                process depending on the scheduling strategy.
            flow_control:
                The flow control settings. Use this to prevent situations where you are
                inundated with too many messages at once.
            scheduler:
                An optional *scheduler* to use when executing the callback. This
                controls how callbacks are executed concurrently. This object must not
                be shared across multiple ``SubscriberClient`` instances.
            use_legacy_flow_control (bool):
                If set to ``True``, flow control at the Cloud Pub/Sub server is disabled,
                though client-side flow control is still enabled. If set to ``False``
                (default), both server-side and client-side flow control are enabled.
            await_callbacks_on_shutdown:
                If ``True``, after canceling the returned future, the latter's
                ``result()`` method will block until the background stream and its
                helper threads have been terminated, and all currently executing message
                callbacks are done processing.

                If ``False`` (default), the returned future's ``result()`` method will
                not block after canceling the future. The method will instead return
                immediately after the background stream and its helper threads have been
                terminated, but some of the message callback threads might still be
                running at that point.

        Returns:
            A future instance that can be used to manage the background stream.
        """
        flow_control = types.FlowControl(*flow_control)

        manager = streaming_pull_manager.StreamingPullManager(
            self,
            subscription,
            flow_control=flow_control,
            scheduler=scheduler,
            use_legacy_flow_control=use_legacy_flow_control,
            await_callbacks_on_shutdown=await_callbacks_on_shutdown,
        )

        future = futures.StreamingPullFuture(manager)

        manager.open(callback=callback, on_callback_error=future.set_exception)

        return future

    def close(self) -> None:
        """Close the underlying channel to release socket resources.

        After a channel has been closed, the client instance cannot be used
        anymore.

        This method is idempotent.
        """
        self.api._transport.grpc_channel.close()
        self._closed = True

    def __enter__(self) -> "Client":
        if self._closed:
            raise RuntimeError("Closed subscriber cannot be used as context manager.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
