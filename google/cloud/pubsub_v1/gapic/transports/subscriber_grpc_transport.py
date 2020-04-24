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


import google.api_core.grpc_helpers

from google.cloud.pubsub_v1.proto import pubsub_pb2_grpc
from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2_grpc


class SubscriberGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.pubsub.v1 Subscriber API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    def __init__(
        self, channel=None, credentials=None, address="pubsub.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "iam_policy_stub": iam_policy_pb2_grpc.IAMPolicyStub(channel),
            "subscriber_stub": pubsub_pb2_grpc.SubscriberStub(channel),
        }

    @classmethod
    def create_channel(
        cls, address="pubsub.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_subscription(self):
        """Return the gRPC stub for :meth:`SubscriberClient.create_subscription`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].CreateSubscription

    @property
    def get_subscription(self):
        """Return the gRPC stub for :meth:`SubscriberClient.get_subscription`.

        Gets the configuration details of a subscription.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].GetSubscription

    @property
    def update_subscription(self):
        """Return the gRPC stub for :meth:`SubscriberClient.update_subscription`.

        Updates an existing subscription. Note that certain properties of a
        subscription, such as its topic, are not modifiable.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].UpdateSubscription

    @property
    def list_subscriptions(self):
        """Return the gRPC stub for :meth:`SubscriberClient.list_subscriptions`.

        Lists matching subscriptions.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].ListSubscriptions

    @property
    def delete_subscription(self):
        """Return the gRPC stub for :meth:`SubscriberClient.delete_subscription`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].DeleteSubscription

    @property
    def get_snapshot(self):
        """Return the gRPC stub for :meth:`SubscriberClient.get_snapshot`.

        Gets the configuration details of a snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow you to manage message acknowledgments in bulk. That
        is, you can set the acknowledgment state of messages in an existing
        subscription to the state captured by a snapshot.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].GetSnapshot

    @property
    def modify_ack_deadline(self):
        """Return the gRPC stub for :meth:`SubscriberClient.modify_ack_deadline`.

        If true, messages published with the same ``ordering_key`` in
        ``PubsubMessage`` will be delivered to the subscribers in the order in
        which they are received by the Pub/Sub system. Otherwise, they may be
        delivered in any order. EXPERIMENTAL: This feature is part of a closed
        alpha release. This API might be changed in backward-incompatible ways
        and is not recommended for production use. It is not subject to any SLA
        or deprecation policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].ModifyAckDeadline

    @property
    def acknowledge(self):
        """Return the gRPC stub for :meth:`SubscriberClient.acknowledge`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].Acknowledge

    @property
    def pull(self):
        """Return the gRPC stub for :meth:`SubscriberClient.pull`.

        Required. The name of the subscription. Format is
        ``projects/{project}/subscriptions/{sub}``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].Pull

    @property
    def streaming_pull(self):
        """Return the gRPC stub for :meth:`SubscriberClient.streaming_pull`.

        ID of this message, assigned by the server when the message is
        published. Guaranteed to be unique within the topic. This value may be
        read by a subscriber that receives a ``PubsubMessage`` via a ``Pull``
        call or a push delivery. It must not be populated by the publisher in a
        ``Publish`` call.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].StreamingPull

    @property
    def modify_push_config(self):
        """Return the gRPC stub for :meth:`SubscriberClient.modify_push_config`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].ModifyPushConfig

    @property
    def list_snapshots(self):
        """Return the gRPC stub for :meth:`SubscriberClient.list_snapshots`.

        Lists the existing snapshots. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].ListSnapshots

    @property
    def create_snapshot(self):
        """Return the gRPC stub for :meth:`SubscriberClient.create_snapshot`.

        The time at which the message was published, populated by the server
        when it receives the ``Publish`` call. It must not be populated by the
        publisher in a ``Publish`` call.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].CreateSnapshot

    @property
    def update_snapshot(self):
        """Return the gRPC stub for :meth:`SubscriberClient.update_snapshot`.

        Updates an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].UpdateSnapshot

    @property
    def delete_snapshot(self):
        """Return the gRPC stub for :meth:`SubscriberClient.delete_snapshot`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].DeleteSnapshot

    @property
    def seek(self):
        """Return the gRPC stub for :meth:`SubscriberClient.seek`.

        Seeks an existing subscription to a point in time or to a given snapshot,
        whichever is provided in the request. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot. Note that both the subscription and the snapshot
        must be on the same topic.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].Seek

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`SubscriberClient.set_iam_policy`.

        Sets the access control policy on the specified resource. Replaces
        any existing policy.

        Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED`
        errors.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`SubscriberClient.get_iam_policy`.

        Gets the access control policy for a resource. Returns an empty policy
        if the resource exists and does not have a policy set.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`SubscriberClient.test_iam_permissions`.

        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of
        permissions, not a `NOT_FOUND` error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].TestIamPermissions
