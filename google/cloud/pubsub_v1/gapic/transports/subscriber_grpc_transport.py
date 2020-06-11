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

        Request for the ``Pull`` method.

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

        Response message for ``TestIamPermissions`` method.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].ModifyAckDeadline

    @property
    def acknowledge(self):
        """Return the gRPC stub for :meth:`SubscriberClient.acknowledge`.

        The resource type. It must be in the format of
        {service_name}/{resource_type_kind}. The ``resource_type_kind`` must be
        singular and must not include version numbers.

        Example: ``storage.googleapis.com/Bucket``

        The value of the resource_type_kind must follow the regular expression
        /[A-Za-z][a-zA-Z0-9]+/. It should start with an upper case character and
        should use PascalCase (UpperCamelCase). The maximum number of characters
        allowed for the ``resource_type_kind`` is 100.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].Acknowledge

    @property
    def pull(self):
        """Return the gRPC stub for :meth:`SubscriberClient.pull`.

        Required. The subscription from which messages should be pulled.
        Format is ``projects/{project}/subscriptions/{sub}``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].Pull

    @property
    def streaming_pull(self):
        """Return the gRPC stub for :meth:`SubscriberClient.streaming_pull`.

        A subset of ``TestPermissionsRequest.permissions`` that the caller
        is allowed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["subscriber_stub"].StreamingPull

    @property
    def modify_push_config(self):
        """Return the gRPC stub for :meth:`SubscriberClient.modify_push_config`.

        Denotes a field as required. This indicates that the field **must**
        be provided as part of the request, and failure to do so will cause an
        error (usually ``INVALID_ARGUMENT``).

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
