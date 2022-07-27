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
    "PublishResponse",
    "ListTopicsResponse",
    "ListTopicSubscriptionsResponse",
    "ListTopicSnapshotsResponse",
    "DetachSubscriptionResponse",
    "ListSubscriptionsResponse",
    "PullResponse",
    "StreamingPullResponse",
    "ListSnapshotsResponse",
    "SeekResponse",
)


class PublishResponse(proto.Message):
    r"""Response for the ``Publish`` method.

    Attributes:
        message_ids (Sequence[str]):
            The server-assigned ID of each published
            message, in the same order as the messages in
            the request. IDs are guaranteed to be unique
            within the topic.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    message_ids = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class ListTopicsResponse(proto.Message):
    r"""Response for the ``ListTopics`` method.

    Attributes:
        topics (Sequence[google.pubsub_v1.types.Topic]):
            The resulting topics.
        next_page_token (str):
            If not empty, indicates that there may be more topics that
            match the request; this value should be passed in a new
            ``ListTopicsRequest``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    topics = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Topic",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListTopicSubscriptionsResponse(proto.Message):
    r"""Response for the ``ListTopicSubscriptions`` method.

    Attributes:
        subscriptions (Sequence[str]):
            The names of subscriptions attached to the
            topic specified in the request.
        next_page_token (str):
            If not empty, indicates that there may be more subscriptions
            that match the request; this value should be passed in a new
            ``ListTopicSubscriptionsRequest`` to get more subscriptions.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    subscriptions = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListTopicSnapshotsResponse(proto.Message):
    r"""Response for the ``ListTopicSnapshots`` method.

    Attributes:
        snapshots (Sequence[str]):
            The names of the snapshots that match the
            request.
        next_page_token (str):
            If not empty, indicates that there may be more snapshots
            that match the request; this value should be passed in a new
            ``ListTopicSnapshotsRequest`` to get more snapshots.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    snapshots = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class DetachSubscriptionResponse(proto.Message):
    r"""Response for the DetachSubscription method.
    Reserved for future use.

    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class ListSubscriptionsResponse(proto.Message):
    r"""Response for the ``ListSubscriptions`` method.

    Attributes:
        subscriptions (Sequence[google.pubsub_v1.types.Subscription]):
            The subscriptions that match the request.
        next_page_token (str):
            If not empty, indicates that there may be more subscriptions
            that match the request; this value should be passed in a new
            ``ListSubscriptionsRequest`` to get more subscriptions.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    subscriptions = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class PullResponse(proto.Message):
    r"""Response for the ``Pull`` method.

    Attributes:
        received_messages (Sequence[google.pubsub_v1.types.ReceivedMessage]):
            Received Pub/Sub messages. The list will be empty if there
            are no more messages available in the backlog. For JSON, the
            response can be entirely empty. The Pub/Sub system may
            return fewer than the ``maxMessages`` requested even if
            there are more messages available in the backlog.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    received_messages = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ReceivedMessage",
    )


class StreamingPullResponse(proto.Message):
    r"""Response for the ``StreamingPull`` method. This response is used to
    stream messages from the server to the client.

    Attributes:
        received_messages (Sequence[google.pubsub_v1.types.ReceivedMessage]):
            Received Pub/Sub messages. This will not be
            empty.
        acknowledge_confirmation (google.pubsub_v1.types.StreamingPullResponse.AcknowledgeConfirmation):
            This field will only be set if
            ``enable_exactly_once_delivery`` is set to ``true``.
        modify_ack_deadline_confirmation (google.pubsub_v1.types.StreamingPullResponse.ModifyAckDeadlineConfirmation):
            This field will only be set if
            ``enable_exactly_once_delivery`` is set to ``true``.
        subscription_properties (google.pubsub_v1.types.StreamingPullResponse.SubscriptionProperties):
            Properties associated with this subscription.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    class AcknowledgeConfirmation(proto.Message):
        r"""Acknowledgement IDs sent in one or more previous requests to
        acknowledge a previously received message.

        Attributes:
            ack_ids (Sequence[str]):
                Successfully processed acknowledgement IDs.
            invalid_ack_ids (Sequence[str]):
                List of acknowledgement IDs that were
                malformed or whose acknowledgement deadline has
                expired.
            unordered_ack_ids (Sequence[str]):
                List of acknowledgement IDs that were out of
                order.
        """
        __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

        ack_ids = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        invalid_ack_ids = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        unordered_ack_ids = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    class ModifyAckDeadlineConfirmation(proto.Message):
        r"""Acknowledgement IDs sent in one or more previous requests to
        modify the deadline for a specific message.

        Attributes:
            ack_ids (Sequence[str]):
                Successfully processed acknowledgement IDs.
            invalid_ack_ids (Sequence[str]):
                List of acknowledgement IDs that were
                malformed or whose acknowledgement deadline has
                expired.
        """
        __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

        ack_ids = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        invalid_ack_ids = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class SubscriptionProperties(proto.Message):
        r"""Subscription properties sent as part of the response.

        Attributes:
            exactly_once_delivery_enabled (bool):
                True iff exactly once delivery is enabled for
                this subscription.
            message_ordering_enabled (bool):
                True iff message ordering is enabled for this
                subscription.
        """
        __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

        exactly_once_delivery_enabled = proto.Field(
            proto.BOOL,
            number=1,
        )
        message_ordering_enabled = proto.Field(
            proto.BOOL,
            number=2,
        )

    received_messages = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ReceivedMessage",
    )
    acknowledge_confirmation = proto.Field(
        proto.MESSAGE,
        number=5,
        message=AcknowledgeConfirmation,
    )
    modify_ack_deadline_confirmation = proto.Field(
        proto.MESSAGE,
        number=3,
        message=ModifyAckDeadlineConfirmation,
    )
    subscription_properties = proto.Field(
        proto.MESSAGE,
        number=4,
        message=SubscriptionProperties,
    )


class ListSnapshotsResponse(proto.Message):
    r"""Response for the ``ListSnapshots`` method.

    Attributes:
        snapshots (Sequence[google.pubsub_v1.types.Snapshot]):
            The resulting snapshots.
        next_page_token (str):
            If not empty, indicates that there may be more snapshot that
            match the request; this value should be passed in a new
            ``ListSnapshotsRequest``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    snapshots = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Snapshot",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class SeekResponse(proto.Message):
    r"""Response for the ``Seek`` method (this response is empty)."""
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


__all__ = tuple(sorted(__manifest__))
