# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.pubsub.v1 Subscriber API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.pubsub_v1.gapic import subscriber_client_config
from google.cloud.pubsub_v1.gapic.transports import subscriber_grpc_transport
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.cloud.pubsub_v1.proto import pubsub_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import iam_policy_pb2_grpc
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-pubsub").version


class SubscriberClient(object):
    """
    Received Pub/Sub messages. The list will be empty if there are no
    more messages available in the backlog. For JSON, the response can be
    entirely empty. The Pub/Sub system may return fewer than the
    ``maxMessages`` requested even if there are more messages available in
    the backlog.
    """

    SERVICE_ADDRESS = "pubsub.googleapis.com:443"
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.pubsub.v1.Subscriber"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SubscriberClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def snapshot_path(cls, project, snapshot):
        """Return a fully-qualified snapshot string."""
        return google.api_core.path_template.expand(
            "projects/{project}/snapshots/{snapshot}",
            project=project,
            snapshot=snapshot,
        )

    @classmethod
    def subscription_path(cls, project, subscription):
        """Return a fully-qualified subscription string."""
        return google.api_core.path_template.expand(
            "projects/{project}/subscriptions/{subscription}",
            project=project,
            subscription=subscription,
        )

    @classmethod
    def topic_path(cls, project, topic):
        """Return a fully-qualified topic string."""
        return google.api_core.path_template.expand(
            "projects/{project}/topics/{topic}", project=project, topic=topic
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.SubscriberGrpcTransport,
                    Callable[[~.Credentials, type], ~.SubscriberGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = subscriber_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=subscriber_grpc_transport.SubscriberGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = subscriber_grpc_transport.SubscriberGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_subscription(
        self,
        name,
        topic,
        push_config=None,
        ack_deadline_seconds=None,
        retain_acked_messages=None,
        message_retention_duration=None,
        labels=None,
        enable_message_ordering=None,
        expiration_policy=None,
        filter_=None,
        dead_letter_policy=None,
        retry_policy=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The time to seek to. Messages retained in the subscription that were
        published before this time are marked as acknowledged, and messages
        retained in the subscription that were published after this time are
        marked as unacknowledged. Note that this operation affects only those
        messages retained in the subscription (configured by the combination of
        ``message_retention_duration`` and ``retain_acked_messages``). For
        example, if ``time`` corresponds to a point before the message retention
        window (or to a point before the system's notion of the subscription
        creation time), only retained messages will be marked as unacknowledged,
        and already-expunged messages will not be restored.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> name = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.create_subscription(name, topic)

        Args:
            name (str): The plural name used in the resource name, such as 'projects' for
                the name of 'projects/{project}'. It is the same concept of the
                ``plural`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/
            topic (str): Set true to use the old proto1 MessageSet wire format for
                extensions. This is provided for backwards-compatibility with the
                MessageSet wire format. You should not use this for any other reason:
                It's less efficient, has fewer features, and is more complicated.

                The message must be defined exactly as follows: message Foo { option
                message_set_wire_format = true; extensions 4 to max; } Note that the
                message cannot have any defined fields; MessageSets only have
                extensions.

                All extensions of your type must be singular messages; e.g. they cannot
                be int32s, enums, or repeated messages.

                Because this is an option, the above two restrictions are not enforced
                by the protocol compiler.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): The service that an application uses to manipulate subscriptions and
                to consume messages from a subscription via the ``Pull`` method or by
                establishing a bi-directional stream using the ``StreamingPull`` method.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            ack_deadline_seconds (int): If non-empty, identifies related messages for which publish order
                should be respected. If a ``Subscription`` has
                ``enable_message_ordering`` set to ``true``, messages published with the
                same non-empty ``ordering_key`` value will be delivered to subscribers
                in the order in which they are received by the Pub/Sub system. All
                ``PubsubMessage``\ s published in a given ``PublishRequest`` must
                specify the same ``ordering_key`` value. EXPERIMENTAL: This feature is
                part of a closed alpha release. This API might be changed in
                backward-incompatible ways and is not recommended for production use. It
                is not subject to any SLA or deprecation policy.
            retain_acked_messages (bool): The same concept of the ``singular`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/
                Such as "project" for the ``resourcemanager.googleapis.com/Project``
                type.
            message_retention_duration (Union[dict, ~google.cloud.pubsub_v1.types.Duration]): Required. The new ack deadline with respect to the time this request
                was sent to the Pub/Sub system. For example, if the value is 10, the new
                ack deadline will expire 10 seconds after the ``ModifyAckDeadline`` call
                was made. Specifying zero might immediately make the message available
                for delivery to another subscriber client. This typically results in an
                increase in the rate of message redeliveries (that is, duplicates). The
                minimum deadline you can specify is 0 seconds. The maximum deadline you
                can specify is 600 seconds (10 minutes).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Duration`
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            enable_message_ordering (bool): Required. The name of the topic to get. Format is
                ``projects/{project}/topics/{topic}``.
            expiration_policy (Union[dict, ~google.cloud.pubsub_v1.types.ExpirationPolicy]): The resource type that the annotated field references.

                Example:

                ::

                    message Subscription {
                      string topic = 2 [(google.api.resource_reference) = {
                        type: "pubsub.googleapis.com/Topic"
                      }];
                    }

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.ExpirationPolicy`
            filter_ (str): Response for the ``Publish`` method.
            dead_letter_policy (Union[dict, ~google.cloud.pubsub_v1.types.DeadLetterPolicy]): Pulls messages from the server. The server may return
                ``UNAVAILABLE`` if there are too many concurrent pull requests pending
                for the given subscription.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.DeadLetterPolicy`
            retry_policy (Union[dict, ~google.cloud.pubsub_v1.types.RetryPolicy]): A policy that specifies how Cloud Pub/Sub retries message delivery for this
                subscription.

                If not set, the default retry policy is applied. This generally implies
                that messages will be retried as soon as possible for healthy subscribers.
                RetryPolicy will be triggered on NACKs or acknowledgement deadline
                exceeded events for a given message.
                <b>EXPERIMENTAL:</b> This API might be changed in backward-incompatible
                ways and is not recommended for production use. It is not subject to any
                SLA or deprecation policy.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.RetryPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_subscription,
                default_retry=self._method_configs["CreateSubscription"].retry,
                default_timeout=self._method_configs["CreateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.Subscription(
            name=name,
            topic=topic,
            push_config=push_config,
            ack_deadline_seconds=ack_deadline_seconds,
            retain_acked_messages=retain_acked_messages,
            message_retention_duration=message_retention_duration,
            labels=labels,
            enable_message_ordering=enable_message_ordering,
            expiration_policy=expiration_policy,
            filter=filter_,
            dead_letter_policy=dead_letter_policy,
            retry_policy=retry_policy,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_subscription(
        self,
        subscription,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the configuration details of a subscription.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.get_subscription(subscription)

        Args:
            subscription (str): Required. The subscription for which to initialize the new stream.
                This must be provided in the first request on the stream, and must not
                be set in subsequent requests from client to server. Format is
                ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_subscription,
                default_retry=self._method_configs["GetSubscription"].retry,
                default_timeout=self._method_configs["GetSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.GetSubscriptionRequest(subscription=subscription)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_subscription(
        self,
        subscription,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing subscription. Note that certain properties of a
        subscription, such as its topic, are not modifiable.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> ack_deadline_seconds = 42
            >>> subscription = {'ack_deadline_seconds': ack_deadline_seconds}
            >>> paths_element = 'ack_deadline_seconds'
            >>> paths = [paths_element]
            >>> update_mask = {'paths': paths}
            >>>
            >>> response = client.update_subscription(subscription, update_mask)

        Args:
            subscription (Union[dict, ~google.cloud.pubsub_v1.types.Subscription]): Required. The updated subscription object.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Subscription`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Required. Indicates which fields in the provided subscription to update.
                Must be specified and non-empty.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_subscription,
                default_retry=self._method_configs["UpdateSubscription"].retry,
                default_timeout=self._method_configs["UpdateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.UpdateSubscriptionRequest(
            subscription=subscription, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription.name", subscription.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_subscriptions(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists matching subscriptions.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_subscriptions(project):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_subscriptions(project).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): Required. The messages in the request will be published on this
                topic. Format is ``projects/{project}/topics/{topic}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.GRPCIterator` instance.
            An iterable of :class:`~google.cloud.pubsub_v1.types.Subscription` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_subscriptions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_subscriptions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_subscriptions,
                default_retry=self._method_configs["ListSubscriptions"].retry,
                default_timeout=self._method_configs["ListSubscriptions"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListSubscriptionsRequest(
            project=project, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project", project)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_subscriptions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="subscriptions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_subscription(
        self,
        subscription,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Optional. The relative resource name pattern associated with this
        resource type. The DNS prefix of the full resource name shouldn't be
        specified here.

        The path pattern must follow the syntax, which aligns with HTTP binding
        syntax:

        ::

            Template = Segment { "/" Segment } ;
            Segment = LITERAL | Variable ;
            Variable = "{" LITERAL "}" ;

        Examples:

        ::

            - "projects/{project}/topics/{topic}"
            - "projects/{project}/knowledgeBases/{knowledge_base}"

        The components in braces correspond to the IDs for each resource in the
        hierarchy. It is expected that, if multiple patterns are provided, the
        same component name (e.g. "project") refers to IDs of the same type of
        resource.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> client.delete_subscription(subscription)

        Args:
            subscription (str): List of acknowledgement IDs for acknowledging previously received
                messages (received on this stream or a different stream). If an ack ID
                has expired, the corresponding message may be redelivered later.
                Acknowledging a message more than once will not result in an error. If
                the acknowledgement ID is malformed, the stream will be aborted with
                status ``INVALID_ARGUMENT``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_subscription,
                default_retry=self._method_configs["DeleteSubscription"].retry,
                default_timeout=self._method_configs["DeleteSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.DeleteSubscriptionRequest(subscription=subscription)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_snapshot(
        self,
        snapshot,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the configuration details of a snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow you to manage message acknowledgments in bulk. That
        is, you can set the acknowledgment state of messages in an existing
        subscription to the state captured by a snapshot.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> snapshot = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>>
            >>> response = client.get_snapshot(snapshot)

        Args:
            snapshot (str): Request for the ``CreateSnapshot`` method.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_snapshot,
                default_retry=self._method_configs["GetSnapshot"].retry,
                default_timeout=self._method_configs["GetSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.GetSnapshotRequest(snapshot=snapshot)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("snapshot", snapshot)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def modify_ack_deadline(
        self,
        subscription,
        ack_ids,
        ack_deadline_seconds,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        If true, messages published with the same ``ordering_key`` in
        ``PubsubMessage`` will be delivered to the subscribers in the order in
        which they are received by the Pub/Sub system. Otherwise, they may be
        delivered in any order. EXPERIMENTAL: This feature is part of a closed
        alpha release. This API might be changed in backward-incompatible ways
        and is not recommended for production use. It is not subject to any SLA
        or deprecation policy.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `ack_ids`:
            >>> ack_ids = []
            >>>
            >>> # TODO: Initialize `ack_deadline_seconds`:
            >>> ack_deadline_seconds = 0
            >>>
            >>> client.modify_ack_deadline(subscription, ack_ids, ack_deadline_seconds)

        Args:
            subscription (str): Role that is assigned to ``members``. For example, ``roles/viewer``,
                ``roles/editor``, or ``roles/owner``.
            ack_ids (list[str]): Required. List of acknowledgment IDs.
            ack_deadline_seconds (int): List of acknowledgement IDs whose deadline will be modified based on
                the corresponding element in ``modify_deadline_seconds``. This field can
                be used to indicate that more time is needed to process a message by the
                subscriber, or to make the message available for redelivery if the
                processing was interrupted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_ack_deadline" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_ack_deadline"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_ack_deadline,
                default_retry=self._method_configs["ModifyAckDeadline"].retry,
                default_timeout=self._method_configs["ModifyAckDeadline"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ModifyAckDeadlineRequest(
            subscription=subscription,
            ack_ids=ack_ids,
            ack_deadline_seconds=ack_deadline_seconds,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["modify_ack_deadline"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def acknowledge(
        self,
        subscription,
        ack_ids,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a snapshot from the requested subscription. Snapshots are
        used in Seek operations, which allow you to manage message
        acknowledgments in bulk. That is, you can set the acknowledgment state
        of messages in an existing subscription to the state captured by a
        snapshot. If the snapshot already exists, returns ``ALREADY_EXISTS``. If
        the requested subscription doesn't exist, returns ``NOT_FOUND``. If the
        backlog in the subscription is too old -- and the resulting snapshot
        would expire in less than 1 hour -- then ``FAILED_PRECONDITION`` is
        returned. See also the ``Snapshot.expire_time`` field. If the name is
        not provided in the request, the server will assign a random name for
        this snapshot on the same project as the subscription, conforming to the
        `resource name
        format <https://cloud.google.com/pubsub/docs/admin#resource_names>`__.
        The generated name is populated in the returned Snapshot object. Note
        that for REST API requests, you must specify a name in the request.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `ack_ids`:
            >>> ack_ids = []
            >>>
            >>> client.acknowledge(subscription, ack_ids)

        Args:
            subscription (str): Protocol Buffers - Google's data interchange format Copyright 2008
                Google Inc. All rights reserved.
                https://developers.google.com/protocol-buffers/

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions are
                met:

                ::

                    * Redistributions of source code must retain the above copyright

                notice, this list of conditions and the following disclaimer. \*
                Redistributions in binary form must reproduce the above copyright
                notice, this list of conditions and the following disclaimer in the
                documentation and/or other materials provided with the distribution. \*
                Neither the name of Google Inc. nor the names of its contributors may be
                used to endorse or promote products derived from this software without
                specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
                IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
                TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
                PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
                OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
                EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
                PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
                LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
                NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
            ack_ids (list[str]): Specifies the identities requesting access for a Cloud Platform
                resource. ``members`` can have the following values:

                -  ``allUsers``: A special identifier that represents anyone who is on
                   the internet; with or without a Google account.

                -  ``allAuthenticatedUsers``: A special identifier that represents
                   anyone who is authenticated with a Google account or a service
                   account.

                -  ``user:{emailid}``: An email address that represents a specific
                   Google account. For example, ``alice@example.com`` .

                -  ``serviceAccount:{emailid}``: An email address that represents a
                   service account. For example,
                   ``my-other-app@appspot.gserviceaccount.com``.

                -  ``group:{emailid}``: An email address that represents a Google group.
                   For example, ``admins@example.com``.

                -  ``domain:{domain}``: The G Suite domain (primary) that represents all
                   the users of that domain. For example, ``google.com`` or
                   ``example.com``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "acknowledge" not in self._inner_api_calls:
            self._inner_api_calls[
                "acknowledge"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.acknowledge,
                default_retry=self._method_configs["Acknowledge"].retry,
                default_timeout=self._method_configs["Acknowledge"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.AcknowledgeRequest(
            subscription=subscription, ack_ids=ack_ids
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["acknowledge"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def pull(
        self,
        subscription,
        max_messages,
        return_immediately=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Required. The name of the subscription. Format is
        ``projects/{project}/subscriptions/{sub}``.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `max_messages`:
            >>> max_messages = 0
            >>>
            >>> response = client.pull(subscription, max_messages)

        Args:
            subscription (str): The approximate amount of time (on a best-effort basis) Pub/Sub
                waits for the subscriber to acknowledge receipt before resending the
                message. In the interval after the message is delivered and before it is
                acknowledged, it is considered to be outstanding. During that time
                period, the message will not be redelivered (on a best-effort basis).

                For pull subscriptions, this value is used as the initial value for the
                ack deadline. To override this value for a given message, call
                ``ModifyAckDeadline`` with the corresponding ``ack_id`` if using
                non-streaming pull or send the ``ack_id`` in a
                ``StreamingModifyAckDeadlineRequest`` if using streaming pull. The
                minimum custom deadline you can specify is 10 seconds. The maximum
                custom deadline you can specify is 600 seconds (10 minutes). If this
                parameter is 0, a default value of 10 seconds is used.

                For push delivery, this value is also used to set the request timeout
                for the call to the push endpoint.

                If the subscriber never acknowledges the message, the Pub/Sub system
                will eventually redeliver the message.
            max_messages (int): Required. The maximum number of messages to return for this request. Must
                be a positive integer. The Pub/Sub system may return fewer than the number
                specified.
            return_immediately (bool): Signed fractions of a second at nanosecond resolution of the span of
                time. Durations less than one second are represented with a 0
                ``seconds`` field and a positive or negative ``nanos`` field. For
                durations of one second or more, a non-zero value for the ``nanos``
                field must be of the same sign as the ``seconds`` field. Must be from
                -999,999,999 to +999,999,999 inclusive.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.PullResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "pull" not in self._inner_api_calls:
            self._inner_api_calls["pull"] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.pull,
                default_retry=self._method_configs["Pull"].retry,
                default_timeout=self._method_configs["Pull"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.PullRequest(
            subscription=subscription,
            max_messages=max_messages,
            return_immediately=return_immediately,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["pull"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def streaming_pull(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ID of this message, assigned by the server when the message is
        published. Guaranteed to be unique within the topic. This value may be
        read by a subscriber that receives a ``PubsubMessage`` via a ``Pull``
        call or a push delivery. It must not be populated by the publisher in a
        ``Publish`` call.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `stream_ack_deadline_seconds`:
            >>> stream_ack_deadline_seconds = 0
            >>> request = {'subscription': subscription, 'stream_ack_deadline_seconds': stream_ack_deadline_seconds}
            >>>
            >>> requests = [request]
            >>> for element in client.streaming_pull(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.pubsub_v1.proto.pubsub_pb2.StreamingPullRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.pubsub_v1.types.StreamingPullRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.pubsub_v1.types.StreamingPullResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "streaming_pull" not in self._inner_api_calls:
            self._inner_api_calls[
                "streaming_pull"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.streaming_pull,
                default_retry=self._method_configs["StreamingPull"].retry,
                default_timeout=self._method_configs["StreamingPull"].timeout,
                client_info=self._client_info,
            )

            # Wrappers in api-core should not automatically pre-fetch the first
            # stream result, as this breaks the stream when re-opening it.
            # https://github.com/googleapis/python-pubsub/issues/93#issuecomment-630762257
            self.transport.streaming_pull._prefetch_first_result_ = False

        return self._inner_api_calls["streaming_pull"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )

    def modify_push_config(
        self,
        subscription,
        push_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Optional. The historical or future-looking state of the resource
        pattern.

        Example:

        ::

            // The InspectTemplate message originally only supported resource
            // names with organization, and project was added later.
            message InspectTemplate {
              option (google.api.resource) = {
                type: "dlp.googleapis.com/InspectTemplate"
                pattern:
                "organizations/{organization}/inspectTemplates/{inspect_template}"
                pattern: "projects/{project}/inspectTemplates/{inspect_template}"
                history: ORIGINALLY_SINGLE_PATTERN
              };
            }

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `push_config`:
            >>> push_config = {}
            >>>
            >>> client.modify_push_config(subscription, push_config)

        Args:
            subscription (str): Response for the ``ListTopicSubscriptions`` method.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): Signed seconds of the span of time. Must be from -315,576,000,000 to
                +315,576,000,000 inclusive. Note: these bounds are computed from: 60
                sec/min \* 60 min/hr \* 24 hr/day \* 365.25 days/year \* 10000 years

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_push_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_push_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_push_config,
                default_retry=self._method_configs["ModifyPushConfig"].retry,
                default_timeout=self._method_configs["ModifyPushConfig"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ModifyPushConfigRequest(
            subscription=subscription, push_config=push_config
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["modify_push_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_snapshots(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the existing snapshots. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_snapshots(project):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_snapshots(project).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): Required. User-provided name for this snapshot. If the name is not
                provided in the request, the server will assign a random name for this
                snapshot on the same project as the subscription. Note that for REST API
                requests, you must specify a name. See the resource name rules. Format
                is ``projects/{project}/snapshots/{snap}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.GRPCIterator` instance.
            An iterable of :class:`~google.cloud.pubsub_v1.types.Snapshot` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_snapshots" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_snapshots"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_snapshots,
                default_retry=self._method_configs["ListSnapshots"].retry,
                default_timeout=self._method_configs["ListSnapshots"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListSnapshotsRequest(project=project, page_size=page_size)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project", project)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_snapshots"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="snapshots",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_snapshot(
        self,
        name,
        subscription,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The time at which the message was published, populated by the server
        when it receives the ``Publish`` call. It must not be populated by the
        publisher in a ``Publish`` call.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> name = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.create_snapshot(name, subscription)

        Args:
            name (str): The value returned by the last ``ListTopicsResponse``; indicates
                that this is a continuation of a prior ``ListTopics`` call, and that the
                system should return the next page of data.
            subscription (str): Protocol Buffers - Google's data interchange format Copyright 2008
                Google Inc. All rights reserved.
                https://developers.google.com/protocol-buffers/

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions are
                met:

                ::

                    * Redistributions of source code must retain the above copyright

                notice, this list of conditions and the following disclaimer. \*
                Redistributions in binary form must reproduce the above copyright
                notice, this list of conditions and the following disclaimer in the
                documentation and/or other materials provided with the distribution. \*
                Neither the name of Google Inc. nor the names of its contributors may be
                used to endorse or promote products derived from this software without
                specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
                IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
                TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
                PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
                OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
                EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
                PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
                LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
                NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_snapshot,
                default_retry=self._method_configs["CreateSnapshot"].retry,
                default_timeout=self._method_configs["CreateSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.CreateSnapshotRequest(
            name=name, subscription=subscription, labels=labels
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_snapshot(
        self,
        snapshot,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> seconds = 123456
            >>> expire_time = {'seconds': seconds}
            >>> snapshot = {'expire_time': expire_time}
            >>> paths_element = 'expire_time'
            >>> paths = [paths_element]
            >>> update_mask = {'paths': paths}
            >>>
            >>> response = client.update_snapshot(snapshot, update_mask)

        Args:
            snapshot (Union[dict, ~google.cloud.pubsub_v1.types.Snapshot]): Required. The updated snapshot object.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Snapshot`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Required. Indicates which fields in the provided snapshot to update.
                Must be specified and non-empty.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_snapshot,
                default_retry=self._method_configs["UpdateSnapshot"].retry,
                default_timeout=self._method_configs["UpdateSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.UpdateSnapshotRequest(
            snapshot=snapshot, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("snapshot.name", snapshot.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_snapshot(
        self,
        snapshot,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Removes an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.<br><br>
        When the snapshot is deleted, all messages retained in the snapshot
        are immediately dropped. After a snapshot is deleted, a new one may be
        created with the same name, but the new one has no association with the old
        snapshot or its subscription, unless the same subscription is specified.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> snapshot = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>>
            >>> client.delete_snapshot(snapshot)

        Args:
            snapshot (str): javalite_serializable
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_snapshot,
                default_retry=self._method_configs["DeleteSnapshot"].retry,
                default_timeout=self._method_configs["DeleteSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.DeleteSnapshotRequest(snapshot=snapshot)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("snapshot", snapshot)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def seek(
        self,
        subscription,
        time=None,
        snapshot=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Seeks an existing subscription to a point in time or to a given snapshot,
        whichever is provided in the request. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot. Note that both the subscription and the snapshot
        must be on the same topic.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.seek(subscription)

        Args:
            subscription (str): Required. The subscription to affect.
            time (Union[dict, ~google.cloud.pubsub_v1.types.Timestamp]): ``FieldMask`` represents a set of symbolic field paths, for example:

                ::

                    paths: "f.a"
                    paths: "f.b.d"

                Here ``f`` represents a field in some root message, ``a`` and ``b``
                fields in the message found in ``f``, and ``d`` a field found in the
                message in ``f.b``.

                Field masks are used to specify a subset of fields that should be
                returned by a get operation or modified by an update operation. Field
                masks also have a custom JSON encoding (see below).

                # Field Masks in Projections

                When used in the context of a projection, a response message or
                sub-message is filtered by the API to only contain those fields as
                specified in the mask. For example, if the mask in the previous example
                is applied to a response message as follows:

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                        x : 2
                      }
                      y : 13
                    }
                    z: 8

                The result will not contain specific values for fields x,y and z (their
                value will be set to the default, and omitted in proto text output):

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                      }
                    }

                A repeated field is not allowed except at the last position of a paths
                string.

                If a FieldMask object is not present in a get operation, the operation
                applies to all fields (as if a FieldMask of all fields had been
                specified).

                Note that a field mask does not necessarily apply to the top-level
                response message. In case of a REST get operation, the field mask
                applies directly to the response, but in case of a REST list operation,
                the mask instead applies to each individual message in the returned
                resource list. In case of a REST custom method, other definitions may be
                used. Where the mask applies will be clearly documented together with
                its declaration in the API. In any case, the effect on the returned
                resource/resources is required behavior for APIs.

                # Field Masks in Update Operations

                A field mask in update operations specifies which fields of the targeted
                resource are going to be updated. The API is required to only change the
                values of the fields as specified in the mask and leave the others
                untouched. If a resource is passed in to describe the updated values,
                the API ignores the values of all fields not covered by the mask.

                If a repeated field is specified for an update operation, new values
                will be appended to the existing repeated field in the target resource.
                Note that a repeated field is only allowed in the last position of a
                ``paths`` string.

                If a sub-message is specified in the last position of the field mask for
                an update operation, then new value will be merged into the existing
                sub-message in the target resource.

                For example, given the target message:

                ::

                    f {
                      b {
                        d: 1
                        x: 2
                      }
                      c: [1]
                    }

                And an update message:

                ::

                    f {
                      b {
                        d: 10
                      }
                      c: [2]
                    }

                then if the field mask is:

                paths: ["f.b", "f.c"]

                then the result will be:

                ::

                    f {
                      b {
                        d: 10
                        x: 2
                      }
                      c: [1, 2]
                    }

                An implementation may provide options to override this default behavior
                for repeated and message fields.

                In order to reset a field's value to the default, the field must be in
                the mask and set to the default value in the provided resource. Hence,
                in order to reset all fields of a resource, provide a default instance
                of the resource and set all fields in the mask, or do not provide a mask
                as described below.

                If a field mask is not present on update, the operation applies to all
                fields (as if a field mask of all fields has been specified). Note that
                in the presence of schema evolution, this may mean that fields the
                client does not know and has therefore not filled into the request will
                be reset to their default. If this is unwanted behavior, a specific
                service may require a client to always specify a field mask, producing
                an error if not.

                As with get operations, the location of the resource which describes the
                updated values in the request message depends on the operation kind. In
                any case, the effect of the field mask is required to be honored by the
                API.

                ## Considerations for HTTP REST

                The HTTP kind of an update operation which uses a field mask must be set
                to PATCH instead of PUT in order to satisfy HTTP semantics (PUT must
                only be used for full updates).

                # JSON Encoding of Field Masks

                In JSON, a field mask is encoded as a single string where paths are
                separated by a comma. Fields name in each path are converted to/from
                lower-camel naming conventions.

                As an example, consider the following message declarations:

                ::

                    message Profile {
                      User user = 1;
                      Photo photo = 2;
                    }
                    message User {
                      string display_name = 1;
                      string address = 2;
                    }

                In proto a field mask for ``Profile`` may look as such:

                ::

                    mask {
                      paths: "user.display_name"
                      paths: "photo"
                    }

                In JSON, the same mask is represented as below:

                ::

                    {
                      mask: "user.displayName,photo"
                    }

                # Field Masks and Oneof Fields

                Field masks treat fields in oneofs just as regular fields. Consider the
                following message:

                ::

                    message SampleMessage {
                      oneof test_oneof {
                        string name = 4;
                        SubMessage sub_message = 9;
                      }
                    }

                The field mask can be:

                ::

                    mask {
                      paths: "name"
                    }

                Or:

                ::

                    mask {
                      paths: "sub_message"
                    }

                Note that oneof type names ("test_oneof" in this case) cannot be used in
                paths.

                ## Field Mask Verification

                The implementation of any API method which has a FieldMask type field in
                the request should verify the included field paths, and return an
                ``INVALID_ARGUMENT`` error if any path is unmappable.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Timestamp`
            snapshot (str): Required. The name of the topic that subscriptions are attached to.
                Format is ``projects/{project}/topics/{topic}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.SeekResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "seek" not in self._inner_api_calls:
            self._inner_api_calls["seek"] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.seek,
                default_retry=self._method_configs["Seek"].retry,
                default_timeout=self._method_configs["Seek"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(time=time, snapshot=snapshot)

        request = pubsub_pb2.SeekRequest(
            subscription=subscription, time=time, snapshot=snapshot
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["seek"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on the specified resource. Replaces
        any existing policy.

        Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED`
        errors.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.pubsub_v1.types.Policy]): See ``HttpRule``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a resource. Returns an empty policy
        if the resource exists and does not have a policy set.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.pubsub_v1.types.GetPolicyOptions]): A URL locating the endpoint to which messages should be pushed. For
                example, a Webhook endpoint might use ``https://example.com/push``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of
        permissions, not a `NOT_FOUND` error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The snapshot is guaranteed to exist up until this time. A
                newly-created snapshot expires no later than 7 days from the time of its
                creation. Its exact lifetime is determined at creation by the existing
                backlog in the source subscription. Specifically, the lifetime of the
                snapshot is
                ``7 days - (age of oldest unacked message in the subscription)``. For
                example, consider a subscription whose oldest unacked message is 3 days
                old. If a snapshot is created from this subscription, the snapshot --
                which will always capture this 3-day-old backlog as long as the snapshot
                exists -- will expire in 4 days. The service will refuse to create a
                snapshot that would expire in less than 1 hour after creation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
