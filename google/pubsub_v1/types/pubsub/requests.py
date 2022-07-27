# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
import proto  # type: ignore

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.pubsub_v1.types import schema as gp_schema

__manifest__ = (
    "GetTopicRequest",
    "UpdateTopicRequest",
    "PublishRequest",
    "ListTopicsRequest",
    "ListTopicSubscriptionsRequest",
    "ListTopicSnapshotsRequest",
    "DeleteTopicRequest",
    "DetachSubscriptionRequest",
    "GetSubscriptionRequest",
    "UpdateSubscriptionRequest",
    "ListSubscriptionsRequest",
    "DeleteSubscriptionRequest",
    "ModifyPushConfigRequest",
    "PullRequest",
    "ModifyAckDeadlineRequest",
    "AcknowledgeRequest",
    "StreamingPullRequest",
    "CreateSnapshotRequest",
    "UpdateSnapshotRequest",
    "GetSnapshotRequest",
    "ListSnapshotsRequest",
    "DeleteSnapshotRequest",
    "SeekRequest",
)


class GetTopicRequest(proto.Message):
    r"""Request for the GetTopic method.

    Attributes:
        topic (str):
            Required. The name of the topic to get. Format is
            ``projects/{project}/topics/{topic}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateTopicRequest(proto.Message):
    r"""Request for the UpdateTopic method.

    Attributes:
        topic (google.pubsub_v1.types.Topic):
            Required. The updated topic object.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Indicates which fields in the provided topic to
            update. Must be specified and non-empty. Note that if
            ``update_mask`` contains "message_storage_policy" but the
            ``message_storage_policy`` is not set in the ``topic``
            provided above, then the updated value is determined by the
            policy configured at the project or organization level.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Topic",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class PublishRequest(proto.Message):
    r"""Request for the Publish method.

    Attributes:
        topic (str):
            Required. The messages in the request will be published on
            this topic. Format is ``projects/{project}/topics/{topic}``.
        messages (Sequence[google.pubsub_v1.types.PubsubMessage]):
            Required. The messages to publish.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.STRING,
        number=1,
    )
    messages = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="PubsubMessage",
    )


class ListTopicsRequest(proto.Message):
    r"""Request for the ``ListTopics`` method.

    Attributes:
        project (str):
            Required. The name of the project in which to list topics.
            Format is ``projects/{project-id}``.
        page_size (int):
            Maximum number of topics to return.
        page_token (str):
            The value returned by the last ``ListTopicsResponse``;
            indicates that this is a continuation of a prior
            ``ListTopics`` call, and that the system should return the
            next page of data.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTopicSubscriptionsRequest(proto.Message):
    r"""Request for the ``ListTopicSubscriptions`` method.

    Attributes:
        topic (str):
            Required. The name of the topic that subscriptions are
            attached to. Format is
            ``projects/{project}/topics/{topic}``.
        page_size (int):
            Maximum number of subscription names to
            return.
        page_token (str):
            The value returned by the last
            ``ListTopicSubscriptionsResponse``; indicates that this is a
            continuation of a prior ``ListTopicSubscriptions`` call, and
            that the system should return the next page of data.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTopicSnapshotsRequest(proto.Message):
    r"""Request for the ``ListTopicSnapshots`` method.

    Attributes:
        topic (str):
            Required. The name of the topic that snapshots are attached
            to. Format is ``projects/{project}/topics/{topic}``.
        page_size (int):
            Maximum number of snapshot names to return.
        page_token (str):
            The value returned by the last
            ``ListTopicSnapshotsResponse``; indicates that this is a
            continuation of a prior ``ListTopicSnapshots`` call, and
            that the system should return the next page of data.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteTopicRequest(proto.Message):
    r"""Request for the ``DeleteTopic`` method.

    Attributes:
        topic (str):
            Required. Name of the topic to delete. Format is
            ``projects/{project}/topics/{topic}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    topic = proto.Field(
        proto.STRING,
        number=1,
    )


class DetachSubscriptionRequest(proto.Message):
    r"""Request for the DetachSubscription method.

    Attributes:
        subscription (str):
            Required. The subscription to detach. Format is
            ``projects/{project}/subscriptions/{subscription}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )


class GetSubscriptionRequest(proto.Message):
    r"""Request for the GetSubscription method.

    Attributes:
        subscription (str):
            Required. The name of the subscription to get. Format is
            ``projects/{project}/subscriptions/{sub}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateSubscriptionRequest(proto.Message):
    r"""Request for the UpdateSubscription method.

    Attributes:
        subscription (google.pubsub_v1.types.Subscription):
            Required. The updated subscription object.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Indicates which fields in the
            provided subscription to update. Must be
            specified and non-empty.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListSubscriptionsRequest(proto.Message):
    r"""Request for the ``ListSubscriptions`` method.

    Attributes:
        project (str):
            Required. The name of the project in which to list
            subscriptions. Format is ``projects/{project-id}``.
        page_size (int):
            Maximum number of subscriptions to return.
        page_token (str):
            The value returned by the last
            ``ListSubscriptionsResponse``; indicates that this is a
            continuation of a prior ``ListSubscriptions`` call, and that
            the system should return the next page of data.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteSubscriptionRequest(proto.Message):
    r"""Request for the DeleteSubscription method.

    Attributes:
        subscription (str):
            Required. The subscription to delete. Format is
            ``projects/{project}/subscriptions/{sub}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )


class ModifyPushConfigRequest(proto.Message):
    r"""Request for the ModifyPushConfig method.

    Attributes:
        subscription (str):
            Required. The name of the subscription. Format is
            ``projects/{project}/subscriptions/{sub}``.
        push_config (google.pubsub_v1.types.PushConfig):
            Required. The push configuration for future deliveries.

            An empty ``pushConfig`` indicates that the Pub/Sub system
            should stop pushing messages from the given subscription and
            allow messages to be pulled and acknowledged - effectively
            pausing the subscription if ``Pull`` or ``StreamingPull`` is
            not called.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    push_config = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PushConfig",
    )


class PullRequest(proto.Message):
    r"""Request for the ``Pull`` method.

    Attributes:
        subscription (str):
            Required. The subscription from which messages should be
            pulled. Format is
            ``projects/{project}/subscriptions/{sub}``.
        return_immediately (bool):
            Optional. If this field set to true, the system will respond
            immediately even if it there are no messages available to
            return in the ``Pull`` response. Otherwise, the system may
            wait (for a bounded amount of time) until at least one
            message is available, rather than returning no messages.
            Warning: setting this field to ``true`` is discouraged
            because it adversely impacts the performance of ``Pull``
            operations. We recommend that users do not set this field.
        max_messages (int):
            Required. The maximum number of messages to
            return for this request. Must be a positive
            integer. The Pub/Sub system may return fewer
            than the number specified.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    return_immediately = proto.Field(
        proto.BOOL,
        number=2,
    )
    max_messages = proto.Field(
        proto.INT32,
        number=3,
    )


class ModifyAckDeadlineRequest(proto.Message):
    r"""Request for the ModifyAckDeadline method.

    Attributes:
        subscription (str):
            Required. The name of the subscription. Format is
            ``projects/{project}/subscriptions/{sub}``.
        ack_ids (Sequence[str]):
            Required. List of acknowledgment IDs.
        ack_deadline_seconds (int):
            Required. The new ack deadline with respect to the time this
            request was sent to the Pub/Sub system. For example, if the
            value is 10, the new ack deadline will expire 10 seconds
            after the ``ModifyAckDeadline`` call was made. Specifying
            zero might immediately make the message available for
            delivery to another subscriber client. This typically
            results in an increase in the rate of message redeliveries
            (that is, duplicates). The minimum deadline you can specify
            is 0 seconds. The maximum deadline you can specify is 600
            seconds (10 minutes).
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    ack_ids = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    ack_deadline_seconds = proto.Field(
        proto.INT32,
        number=3,
    )


class AcknowledgeRequest(proto.Message):
    r"""Request for the Acknowledge method.

    Attributes:
        subscription (str):
            Required. The subscription whose message is being
            acknowledged. Format is
            ``projects/{project}/subscriptions/{sub}``.
        ack_ids (Sequence[str]):
            Required. The acknowledgment ID for the messages being
            acknowledged that was returned by the Pub/Sub system in the
            ``Pull`` response. Must not be empty.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    ack_ids = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class StreamingPullRequest(proto.Message):
    r"""Request for the ``StreamingPull`` streaming RPC method. This request
    is used to establish the initial stream as well as to stream
    acknowledgements and ack deadline modifications from the client to
    the server.

    Attributes:
        subscription (str):
            Required. The subscription for which to initialize the new
            stream. This must be provided in the first request on the
            stream, and must not be set in subsequent requests from
            client to server. Format is
            ``projects/{project}/subscriptions/{sub}``.
        ack_ids (Sequence[str]):
            List of acknowledgement IDs for acknowledging previously
            received messages (received on this stream or a different
            stream). If an ack ID has expired, the corresponding message
            may be redelivered later. Acknowledging a message more than
            once will not result in an error. If the acknowledgement ID
            is malformed, the stream will be aborted with status
            ``INVALID_ARGUMENT``.
        modify_deadline_seconds (Sequence[int]):
            The list of new ack deadlines for the IDs listed in
            ``modify_deadline_ack_ids``. The size of this list must be
            the same as the size of ``modify_deadline_ack_ids``. If it
            differs the stream will be aborted with
            ``INVALID_ARGUMENT``. Each element in this list is applied
            to the element in the same position in
            ``modify_deadline_ack_ids``. The new ack deadline is with
            respect to the time this request was sent to the Pub/Sub
            system. Must be >= 0. For example, if the value is 10, the
            new ack deadline will expire 10 seconds after this request
            is received. If the value is 0, the message is immediately
            made available for another streaming or non-streaming pull
            request. If the value is < 0 (an error), the stream will be
            aborted with status ``INVALID_ARGUMENT``.
        modify_deadline_ack_ids (Sequence[str]):
            List of acknowledgement IDs whose deadline will be modified
            based on the corresponding element in
            ``modify_deadline_seconds``. This field can be used to
            indicate that more time is needed to process a message by
            the subscriber, or to make the message available for
            redelivery if the processing was interrupted.
        stream_ack_deadline_seconds (int):
            Required. The ack deadline to use for the
            stream. This must be provided in the first
            request on the stream, but it can also be
            updated on subsequent requests from client to
            server. The minimum deadline you can specify is
            10 seconds. The maximum deadline you can specify
            is 600 seconds (10 minutes).
        client_id (str):
            A unique identifier that is used to distinguish client
            instances from each other. Only needs to be provided on the
            initial request. When a stream disconnects and reconnects
            for the same stream, the client_id should be set to the same
            value so that state associated with the old stream can be
            transferred to the new stream. The same client_id should not
            be used for different client instances.
        max_outstanding_messages (int):
            Flow control settings for the maximum number of outstanding
            messages. When there are ``max_outstanding_messages`` or
            more currently sent to the streaming pull client that have
            not yet been acked or nacked, the server stops sending more
            messages. The sending of messages resumes once the number of
            outstanding messages is less than this value. If the value
            is <= 0, there is no limit to the number of outstanding
            messages. This property can only be set on the initial
            StreamingPullRequest. If it is set on a subsequent request,
            the stream will be aborted with status ``INVALID_ARGUMENT``.
        max_outstanding_bytes (int):
            Flow control settings for the maximum number of outstanding
            bytes. When there are ``max_outstanding_bytes`` or more
            worth of messages currently sent to the streaming pull
            client that have not yet been acked or nacked, the server
            will stop sending more messages. The sending of messages
            resumes once the number of outstanding bytes is less than
            this value. If the value is <= 0, there is no limit to the
            number of outstanding bytes. This property can only be set
            on the initial StreamingPullRequest. If it is set on a
            subsequent request, the stream will be aborted with status
            ``INVALID_ARGUMENT``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    ack_ids = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    modify_deadline_seconds = proto.RepeatedField(
        proto.INT32,
        number=3,
    )
    modify_deadline_ack_ids = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    stream_ack_deadline_seconds = proto.Field(
        proto.INT32,
        number=5,
    )
    client_id = proto.Field(
        proto.STRING,
        number=6,
    )
    max_outstanding_messages = proto.Field(
        proto.INT64,
        number=7,
    )
    max_outstanding_bytes = proto.Field(
        proto.INT64,
        number=8,
    )


class CreateSnapshotRequest(proto.Message):
    r"""Request for the ``CreateSnapshot`` method.

    Attributes:
        name (str):
            Required. User-provided name for this snapshot. If the name
            is not provided in the request, the server will assign a
            random name for this snapshot on the same project as the
            subscription. Note that for REST API requests, you must
            specify a name. See the resource name rules. Format is
            ``projects/{project}/snapshots/{snap}``.
        subscription (str):
            Required. The subscription whose backlog the snapshot
            retains. Specifically, the created snapshot is guaranteed to
            retain: (a) The existing backlog on the subscription. More
            precisely, this is defined as the messages in the
            subscription's backlog that are unacknowledged upon the
            successful completion of the ``CreateSnapshot`` request; as
            well as: (b) Any messages published to the subscription's
            topic following the successful completion of the
            CreateSnapshot request. Format is
            ``projects/{project}/subscriptions/{sub}``.
        labels (Mapping[str, str]):
            See <a
            href="https://cloud.google.com/pubsub/docs/labels">
            Creating and managing labels</a>.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    subscription = proto.Field(
        proto.STRING,
        number=2,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class UpdateSnapshotRequest(proto.Message):
    r"""Request for the UpdateSnapshot method.

    Attributes:
        snapshot (google.pubsub_v1.types.Snapshot):
            Required. The updated snapshot object.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Indicates which fields in the
            provided snapshot to update. Must be specified
            and non-empty.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    snapshot = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Snapshot",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetSnapshotRequest(proto.Message):
    r"""Request for the GetSnapshot method.

    Attributes:
        snapshot (str):
            Required. The name of the snapshot to get. Format is
            ``projects/{project}/snapshots/{snap}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    snapshot = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSnapshotsRequest(proto.Message):
    r"""Request for the ``ListSnapshots`` method.

    Attributes:
        project (str):
            Required. The name of the project in which to list
            snapshots. Format is ``projects/{project-id}``.
        page_size (int):
            Maximum number of snapshots to return.
        page_token (str):
            The value returned by the last ``ListSnapshotsResponse``;
            indicates that this is a continuation of a prior
            ``ListSnapshots`` call, and that the system should return
            the next page of data.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteSnapshotRequest(proto.Message):
    r"""Request for the ``DeleteSnapshot`` method.

    Attributes:
        snapshot (str):
            Required. The name of the snapshot to delete. Format is
            ``projects/{project}/snapshots/{snap}``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    snapshot = proto.Field(
        proto.STRING,
        number=1,
    )


class SeekRequest(proto.Message):
    r"""Request for the ``Seek`` method.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        subscription (str):
            Required. The subscription to affect.
        time (google.protobuf.timestamp_pb2.Timestamp):
            The time to seek to. Messages retained in the subscription
            that were published before this time are marked as
            acknowledged, and messages retained in the subscription that
            were published after this time are marked as unacknowledged.
            Note that this operation affects only those messages
            retained in the subscription (configured by the combination
            of ``message_retention_duration`` and
            ``retain_acked_messages``). For example, if ``time``
            corresponds to a point before the message retention window
            (or to a point before the system's notion of the
            subscription creation time), only retained messages will be
            marked as unacknowledged, and already-expunged messages will
            not be restored.

            This field is a member of `oneof`_ ``target``.
        snapshot (str):
            The snapshot to seek to. The snapshot's topic must be the
            same as that of the provided subscription. Format is
            ``projects/{project}/snapshots/{snap}``.

            This field is a member of `oneof`_ ``target``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    subscription = proto.Field(
        proto.STRING,
        number=1,
    )
    time = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="target",
        message=timestamp_pb2.Timestamp,
    )
    snapshot = proto.Field(
        proto.STRING,
        number=3,
        oneof="target",
    )


__all__ = tuple(sorted(__manifest__))
