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
    The resource has one pattern, but the API owner expects to add more
    later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
    that from being necessary once there are multiple patterns.)
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
        detached=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request for the ``Pull`` method.

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
            name (str): The resource name of the Cloud KMS CryptoKey to be used to protect
                access to messages published on this topic.

                The expected format is
                ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
            topic (str): Optional. If this field set to true, the system will respond
                immediately even if it there are no messages available to return in the
                ``Pull`` response. Otherwise, the system may wait (for a bounded amount
                of time) until at least one message is available, rather than returning
                no messages. Warning: setting this field to ``true`` is discouraged
                because it adversely impacts the performance of ``Pull`` operations. We
                recommend that users do not set this field.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): Optional. The historical or future-looking state of the resource
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

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            ack_deadline_seconds (int): Response for the ``Publish`` method.
            retain_acked_messages (bool): If set, gives the index of a oneof in the containing type's
                oneof_decl list. This field is a member of that oneof.
            message_retention_duration (Union[dict, ~google.cloud.pubsub_v1.types.Duration]): The plural name used in the resource name and permission names, such
                as 'projects' for the resource name of 'projects/{project}' and the
                permission name of 'cloudresourcemanager.googleapis.com/projects.get'.
                It is the same concept of the ``plural`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/

                Note: The plural form is required even for singleton resources. See
                https://aip.dev/156

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Duration`
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            enable_message_ordering (bool): Set true to use the old proto1 MessageSet wire format for
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
            expiration_policy (Union[dict, ~google.cloud.pubsub_v1.types.ExpirationPolicy]): Denotes a field as output only. This indicates that the field is
                provided in responses, but including the field in a request does nothing
                (the server *must* ignore it and *must not* throw an error as a result
                of the field's presence).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.ExpirationPolicy`
            filter_ (str): Response for the ``Pull`` method.
            dead_letter_policy (Union[dict, ~google.cloud.pubsub_v1.types.DeadLetterPolicy]): The same concept of the ``singular`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/
                Such as "project" for the ``resourcemanager.googleapis.com/Project``
                type.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.DeadLetterPolicy`
            retry_policy (Union[dict, ~google.cloud.pubsub_v1.types.RetryPolicy]): A policy that specifies how Pub/Sub retries message delivery for this
                subscription.

                If not set, the default retry policy is applied. This generally implies
                that messages will be retried as soon as possible for healthy subscribers.
                RetryPolicy will be triggered on NACKs or acknowledgement deadline
                exceeded events for a given message.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.RetryPolicy`
            detached (bool): The time at which the message was published, populated by the server
                when it receives the ``Publish`` call. It must not be populated by the
                publisher in a ``Publish`` call.
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
            detached=detached,
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
            subscription (str): Required. The new ack deadline with respect to the time this request
                was sent to the Pub/Sub system. For example, if the value is 10, the new
                ack deadline will expire 10 seconds after the ``ModifyAckDeadline`` call
                was made. Specifying zero might immediately make the message available
                for delivery to another subscriber client. This typically results in an
                increase in the rate of message redeliveries (that is, duplicates). The
                minimum deadline you can specify is 0 seconds. The maximum deadline you
                can specify is 600 seconds (10 minutes).
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
            >>> subscription_name = 'projects/my-project/subscriptions/my-subscription'
            >>> subscription = {
            ...    'name': subscription_name,
            ...    'ack_deadline_seconds': ack_deadline_seconds,
            ... }
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
            project (str): Required. Indicates which fields in the provided topic to update.
                Must be specified and non-empty. Note that if ``update_mask`` contains
                "message_storage_policy" but the ``message_storage_policy`` is not set
                in the ``topic`` provided above, then the updated value is determined by
                the policy configured at the project or organization level.
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
        Response message for ``TestIamPermissions`` method.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> client.delete_subscription(subscription)

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
            snapshot (str): Protocol Buffers - Google's data interchange format Copyright 2008
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
        If true, this is a proto3 "optional". When a proto3 field is
        optional, it tracks presence regardless of field type.

        When proto3_optional is true, this field must be belong to a oneof to
        signal to old proto3 clients that presence is tracked for this field.
        This oneof is known as a "synthetic" oneof, and this field must be its
        sole member (each proto3 optional field gets its own synthetic oneof).
        Synthetic oneofs exist in the descriptor only, and do not generate any
        API. Synthetic oneofs must be ordered after all "real" oneofs.

        For message fields, proto3_optional doesn't create any semantic change,
        since non-repeated message fields always track presence. However it
        still indicates the semantic detail of whether the user wrote "optional"
        or not. This can be useful for round-tripping the .proto file. For
        consistency we give message fields a synthetic oneof also, even though
        it is not required to track presence. This is especially important
        because the parser can't tell if a field is a message or an enum, so it
        must always create a synthetic oneof.

        Proto2 optional fields do not set this flag, because they already
        indicate optional with ``LABEL_OPTIONAL``.

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
            subscription (str): If this SourceCodeInfo represents a complete declaration, these are
                any comments appearing before and after the declaration which appear to
                be attached to the declaration.

                A series of line comments appearing on consecutive lines, with no other
                tokens appearing on those lines, will be treated as a single comment.

                leading_detached_comments will keep paragraphs of comments that appear
                before (but not connected to) the current element. Each paragraph,
                separated by empty lines, will be one comment element in the repeated
                field.

                Only the comment content is provided; comment markers (e.g. //) are
                stripped out. For block comments, leading whitespace and an asterisk
                will be stripped from the beginning of each line other than the first.
                Newlines are included in the output.

                Examples:

                optional int32 foo = 1; // Comment attached to foo. // Comment attached
                to bar. optional int32 bar = 2;

                optional string baz = 3; // Comment attached to baz. // Another line
                attached to baz.

                // Comment attached to qux. // // Another line attached to qux. optional
                double qux = 4;

                // Detached comment for corge. This is not leading or trailing comments
                // to qux or corge because there are blank lines separating it from //
                both.

                // Detached comment for corge paragraph 2.

                optional string corge = 5; /\* Block comment attached \* to corge.
                Leading asterisks \* will be removed. */ /* Block comment attached to \*
                grault. \*/ optional int32 grault = 6;

                // ignored detached comments.
            ack_ids (list[str]): Required. List of acknowledgment IDs.
            ack_deadline_seconds (int): Specifies the format of the policy.

                Valid values are 0, 1, and 3. Requests specifying an invalid value will
                be rejected.

                Operations affecting conditional bindings must specify version 3. This
                can be either setting a conditional policy, modifying a conditional
                binding, or removing a binding (conditional or unconditional) from the
                stored conditional policy. Operations on non-conditional policies may
                specify any valid value or leave the field unset.

                If no etag is provided in the call to ``setIamPolicy``, version
                compliance checks against the stored policy is skipped.
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
        The resource type. It must be in the format of
        {service_name}/{resource_type_kind}. The ``resource_type_kind`` must be
        singular and must not include version numbers.

        Example: ``storage.googleapis.com/Bucket``

        The value of the resource_type_kind must follow the regular expression
        /[A-Za-z][a-zA-Z0-9]+/. It should start with an upper case character and
        should use PascalCase (UpperCamelCase). The maximum number of characters
        allowed for the ``resource_type_kind`` is 100.

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
            subscription (str): Specifies the log_type that was be enabled. ADMIN_ACTIVITY is always
                enabled, and cannot be configured. Required
            ack_ids (list[str]): If push delivery is used with this subscription, this field is used
                to configure it. An empty ``pushConfig`` signifies that the subscriber
                will pull and ack messages using API methods.
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
        Required. The subscription from which messages should be pulled.
        Format is ``projects/{project}/subscriptions/{sub}``.

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
            subscription (str): Required. The acknowledgment ID for the messages being acknowledged
                that was returned by the Pub/Sub system in the ``Pull`` response. Must
                not be empty.
            max_messages (int): Required. The maximum number of messages to return for this request. Must
                be a positive integer. The Pub/Sub system may return fewer than the number
                specified.
            return_immediately (bool): Required. The name of the topic from which this subscription is
                receiving messages. Format is ``projects/{project}/topics/{topic}``. The
                value of this field will be ``_deleted-topic_`` if the topic has been
                deleted.
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
        A subset of ``TestPermissionsRequest.permissions`` that the caller
        is allowed.

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
        Denotes a field as required. This indicates that the field **must**
        be provided as part of the request, and failure to do so will cause an
        error (usually ``INVALID_ARGUMENT``).

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
            subscription (str): Signed seconds of the span of time. Must be from -315,576,000,000 to
                +315,576,000,000 inclusive. Note: these bounds are computed from: 60
                sec/min \* 60 min/hr \* 24 hr/day \* 365.25 days/year \* 10000 years
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): Required. The messages in the request will be published on this
                topic. Format is ``projects/{project}/topics/{topic}``.

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
            project (str): Specifies the identities requesting access for a Cloud Platform
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
            >>> name = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.create_snapshot(name, subscription)

        Args:
            name (str): Associates ``members`` with a ``role``.
            subscription (str): How long to retain unacknowledged messages in the subscription's
                backlog, from the moment a message is published. If
                ``retain_acked_messages`` is true, then this also configures the
                retention of acknowledged messages, and thus configures how far back in
                time a ``Seek`` can be done. Defaults to 7 days. Cannot be more than 7
                days or less than 10 minutes.
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
            >>> snapshot_name = 'projects/my-project/snapshots/my-snapshot'
            >>> snapshot = {
            ...    'name': snapshot_name,
            ...    'expire_time': expire_time,
            ... }
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
            snapshot (str): An expression written in the Cloud Pub/Sub filter language. If
                non-empty, then only ``PubsubMessage``\ s whose ``attributes`` field
                matches the filter are delivered on this subscription. If empty, then no
                messages are filtered out.
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
            time (Union[dict, ~google.cloud.pubsub_v1.types.Timestamp]): If not empty, indicates that there may be more topics that match the
                request; this value should be passed in a new ``ListTopicsRequest``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Timestamp`
            snapshot (str): Adds one or more messages to the topic. Returns ``NOT_FOUND`` if the
                topic does not exist.
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
            policy (Union[dict, ~google.cloud.pubsub_v1.types.Policy]): Role that is assigned to ``members``. For example, ``roles/viewer``,
                ``roles/editor``, or ``roles/owner``. Required

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
            options_ (Union[dict, ~google.cloud.pubsub_v1.types.GetPolicyOptions]): The name of the topic to which dead letter messages should be
                published. Format is ``projects/{project}/topics/{topic}``.The Cloud
                Pub/Sub service account associated with the enclosing subscription's
                parent project (i.e.,
                service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must
                have permission to Publish() to this topic.

                The operation will fail if the topic does not exist. Users should ensure
                that there is a subscription attached to this topic since messages
                published to a topic with no subscriptions are lost.

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
            permissions (list[str]): See ``HttpRule``.
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
