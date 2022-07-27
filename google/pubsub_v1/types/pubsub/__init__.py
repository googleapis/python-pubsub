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


__protobuf__ = proto.module(
    package="google.pubsub.v1",
    manifest={
        "MessageStoragePolicy",
        "SchemaSettings",
        "Topic",
        "PubsubMessage",
        "GetTopicRequest",
        "UpdateTopicRequest",
        "PublishRequest",
        "PublishResponse",
        "ListTopicsRequest",
        "ListTopicsResponse",
        "ListTopicSubscriptionsRequest",
        "ListTopicSubscriptionsResponse",
        "ListTopicSnapshotsRequest",
        "ListTopicSnapshotsResponse",
        "DeleteTopicRequest",
        "DetachSubscriptionRequest",
        "DetachSubscriptionResponse",
        "Subscription",
        "RetryPolicy",
        "DeadLetterPolicy",
        "ExpirationPolicy",
        "PushConfig",
        "BigQueryConfig",
        "ReceivedMessage",
        "GetSubscriptionRequest",
        "UpdateSubscriptionRequest",
        "ListSubscriptionsRequest",
        "ListSubscriptionsResponse",
        "DeleteSubscriptionRequest",
        "ModifyPushConfigRequest",
        "PullRequest",
        "PullResponse",
        "ModifyAckDeadlineRequest",
        "AcknowledgeRequest",
        "StreamingPullRequest",
        "StreamingPullResponse",
        "CreateSnapshotRequest",
        "UpdateSnapshotRequest",
        "Snapshot",
        "GetSnapshotRequest",
        "ListSnapshotsRequest",
        "ListSnapshotsResponse",
        "DeleteSnapshotRequest",
        "SeekRequest",
        "SeekResponse",
    },
)


from .requests import (
    GetTopicRequest,
    UpdateTopicRequest,
    PublishRequest,
    ListTopicsRequest,
    ListTopicSubscriptionsRequest,
    ListTopicSnapshotsRequest,
    DeleteTopicRequest,
    DetachSubscriptionRequest,
    GetSubscriptionRequest,
    UpdateSubscriptionRequest,
    ListSubscriptionsRequest,
    DeleteSubscriptionRequest,
    ModifyPushConfigRequest,
    PullRequest,
    ModifyAckDeadlineRequest,
    AcknowledgeRequest,
    StreamingPullRequest,
    CreateSnapshotRequest,
    UpdateSnapshotRequest,
    GetSnapshotRequest,
    ListSnapshotsRequest,
    DeleteSnapshotRequest,
    SeekRequest,
)

from .responses import (
    PublishResponse,
    ListTopicsResponse,
    ListTopicSubscriptionsResponse,
    ListTopicSnapshotsResponse,
    DetachSubscriptionResponse,
    ListSubscriptionsResponse,
    PullResponse,
    StreamingPullResponse,
    ListSnapshotsResponse,
    SeekResponse,
)


class MessageStoragePolicy(proto.Message):
    r"""A policy constraining the storage of messages published to
    the topic.

    Attributes:
        allowed_persistence_regions (Sequence[str]):
            A list of IDs of GCP regions where messages
            that are published to the topic may be persisted
            in storage. Messages published by publishers
            running in non-allowed GCP regions (or running
            outside of GCP altogether) will be routed for
            storage in one of the allowed regions. An empty
            list means that no regions are allowed, and is
            not a valid configuration.
    """

    allowed_persistence_regions = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class SchemaSettings(proto.Message):
    r"""Settings for validating messages published against a schema.

    Attributes:
        schema (str):
            Required. The name of the schema that messages published
            should be validated against. Format is
            ``projects/{project}/schemas/{schema}``. The value of this
            field will be ``_deleted-schema_`` if the schema has been
            deleted.
        encoding (google.pubsub_v1.types.Encoding):
            The encoding of messages validated against ``schema``.
    """

    schema = proto.Field(
        proto.STRING,
        number=1,
    )
    encoding = proto.Field(
        proto.ENUM,
        number=2,
        enum=gp_schema.Encoding,
    )


class Topic(proto.Message):
    r"""A topic resource.

    Attributes:
        name (str):
            Required. The name of the topic. It must have the format
            ``"projects/{project}/topics/{topic}"``. ``{topic}`` must
            start with a letter, and contain only letters
            (``[A-Za-z]``), numbers (``[0-9]``), dashes (``-``),
            underscores (``_``), periods (``.``), tildes (``~``), plus
            (``+``) or percent signs (``%``). It must be between 3 and
            255 characters in length, and it must not start with
            ``"goog"``.
        labels (Mapping[str, str]):
            See [Creating and managing labels]
            (https://cloud.google.com/pubsub/docs/labels).
        message_storage_policy (google.pubsub_v1.types.MessageStoragePolicy):
            Policy constraining the set of Google Cloud
            Platform regions where messages published to the
            topic may be stored. If not present, then no
            constraints are in effect.
        kms_key_name (str):
            The resource name of the Cloud KMS CryptoKey to be used to
            protect access to messages published on this topic.

            The expected format is
            ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
        schema_settings (google.pubsub_v1.types.SchemaSettings):
            Settings for validating messages published
            against a schema.
        satisfies_pzs (bool):
            Reserved for future use. This field is set
            only in responses from the server; it is ignored
            if it is set in any requests.
        message_retention_duration (google.protobuf.duration_pb2.Duration):
            Indicates the minimum duration to retain a message after it
            is published to the topic. If this field is set, messages
            published to the topic in the last
            ``message_retention_duration`` are always available to
            subscribers. For instance, it allows any attached
            subscription to `seek to a
            timestamp <https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_time>`__
            that is up to ``message_retention_duration`` in the past. If
            this field is not set, message retention is controlled by
            settings on individual subscriptions. Cannot be more than 7
            days or less than 10 minutes.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    message_storage_policy = proto.Field(
        proto.MESSAGE,
        number=3,
        message="MessageStoragePolicy",
    )
    kms_key_name = proto.Field(
        proto.STRING,
        number=5,
    )
    schema_settings = proto.Field(
        proto.MESSAGE,
        number=6,
        message="SchemaSettings",
    )
    satisfies_pzs = proto.Field(
        proto.BOOL,
        number=7,
    )
    message_retention_duration = proto.Field(
        proto.MESSAGE,
        number=8,
        message=duration_pb2.Duration,
    )


class PubsubMessage(proto.Message):
    r"""A message that is published by publishers and consumed by
    subscribers. The message must contain either a non-empty data field
    or at least one attribute. Note that client libraries represent this
    object differently depending on the language. See the corresponding
    `client library
    documentation <https://cloud.google.com/pubsub/docs/reference/libraries>`__
    for more information. See [quotas and limits]
    (https://cloud.google.com/pubsub/quotas) for more information about
    message limits.

    Attributes:
        data (bytes):
            The message data field. If this field is
            empty, the message must contain at least one
            attribute.
        attributes (Mapping[str, str]):
            Attributes for this message. If this field is
            empty, the message must contain non-empty data.
            This can be used to filter messages on the
            subscription.
        message_id (str):
            ID of this message, assigned by the server when the message
            is published. Guaranteed to be unique within the topic. This
            value may be read by a subscriber that receives a
            ``PubsubMessage`` via a ``Pull`` call or a push delivery. It
            must not be populated by the publisher in a ``Publish``
            call.
        publish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the message was published, populated by
            the server when it receives the ``Publish`` call. It must
            not be populated by the publisher in a ``Publish`` call.
        ordering_key (str):
            If non-empty, identifies related messages for which publish
            order should be respected. If a ``Subscription`` has
            ``enable_message_ordering`` set to ``true``, messages
            published with the same non-empty ``ordering_key`` value
            will be delivered to subscribers in the order in which they
            are received by the Pub/Sub system. All ``PubsubMessage``\ s
            published in a given ``PublishRequest`` must specify the
            same ``ordering_key`` value.
    """

    data = proto.Field(
        proto.BYTES,
        number=1,
    )
    attributes = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    message_id = proto.Field(
        proto.STRING,
        number=3,
    )
    publish_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    ordering_key = proto.Field(
        proto.STRING,
        number=5,
    )


class Subscription(proto.Message):
    r"""A subscription resource.

    Attributes:
        name (str):
            Required. The name of the subscription. It must have the
            format
            ``"projects/{project}/subscriptions/{subscription}"``.
            ``{subscription}`` must start with a letter, and contain
            only letters (``[A-Za-z]``), numbers (``[0-9]``), dashes
            (``-``), underscores (``_``), periods (``.``), tildes
            (``~``), plus (``+``) or percent signs (``%``). It must be
            between 3 and 255 characters in length, and it must not
            start with ``"goog"``.
        topic (str):
            Required. The name of the topic from which this subscription
            is receiving messages. Format is
            ``projects/{project}/topics/{topic}``. The value of this
            field will be ``_deleted-topic_`` if the topic has been
            deleted.
        push_config (google.pubsub_v1.types.PushConfig):
            If push delivery is used with this subscription, this field
            is used to configure it. Either ``pushConfig`` or
            ``bigQueryConfig`` can be set, but not both. If both are
            empty, then the subscriber will pull and ack messages using
            API methods.
        bigquery_config (google.pubsub_v1.types.BigQueryConfig):
            If delivery to BigQuery is used with this subscription, this
            field is used to configure it. Either ``pushConfig`` or
            ``bigQueryConfig`` can be set, but not both. If both are
            empty, then the subscriber will pull and ack messages using
            API methods.
        ack_deadline_seconds (int):
            The approximate amount of time (on a best-effort basis)
            Pub/Sub waits for the subscriber to acknowledge receipt
            before resending the message. In the interval after the
            message is delivered and before it is acknowledged, it is
            considered to be outstanding. During that time period, the
            message will not be redelivered (on a best-effort basis).

            For pull subscriptions, this value is used as the initial
            value for the ack deadline. To override this value for a
            given message, call ``ModifyAckDeadline`` with the
            corresponding ``ack_id`` if using non-streaming pull or send
            the ``ack_id`` in a ``StreamingModifyAckDeadlineRequest`` if
            using streaming pull. The minimum custom deadline you can
            specify is 10 seconds. The maximum custom deadline you can
            specify is 600 seconds (10 minutes). If this parameter is 0,
            a default value of 10 seconds is used.

            For push delivery, this value is also used to set the
            request timeout for the call to the push endpoint.

            If the subscriber never acknowledges the message, the
            Pub/Sub system will eventually redeliver the message.
        retain_acked_messages (bool):
            Indicates whether to retain acknowledged messages. If true,
            then messages are not expunged from the subscription's
            backlog, even if they are acknowledged, until they fall out
            of the ``message_retention_duration`` window. This must be
            true if you would like to [``Seek`` to a timestamp]
            (https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_time)
            in the past to replay previously-acknowledged messages.
        message_retention_duration (google.protobuf.duration_pb2.Duration):
            How long to retain unacknowledged messages in the
            subscription's backlog, from the moment a message is
            published. If ``retain_acked_messages`` is true, then this
            also configures the retention of acknowledged messages, and
            thus configures how far back in time a ``Seek`` can be done.
            Defaults to 7 days. Cannot be more than 7 days or less than
            10 minutes.
        labels (Mapping[str, str]):
            See <a
            href="https://cloud.google.com/pubsub/docs/labels">
            Creating and managing labels</a>.
        enable_message_ordering (bool):
            If true, messages published with the same ``ordering_key``
            in ``PubsubMessage`` will be delivered to the subscribers in
            the order in which they are received by the Pub/Sub system.
            Otherwise, they may be delivered in any order.
        expiration_policy (google.pubsub_v1.types.ExpirationPolicy):
            A policy that specifies the conditions for this
            subscription's expiration. A subscription is considered
            active as long as any connected subscriber is successfully
            consuming messages from the subscription or is issuing
            operations on the subscription. If ``expiration_policy`` is
            not set, a *default policy* with ``ttl`` of 31 days will be
            used. The minimum allowed value for
            ``expiration_policy.ttl`` is 1 day.
        filter (str):
            An expression written in the Pub/Sub `filter
            language <https://cloud.google.com/pubsub/docs/filtering>`__.
            If non-empty, then only ``PubsubMessage``\ s whose
            ``attributes`` field matches the filter are delivered on
            this subscription. If empty, then no messages are filtered
            out.
        dead_letter_policy (google.pubsub_v1.types.DeadLetterPolicy):
            A policy that specifies the conditions for dead lettering
            messages in this subscription. If dead_letter_policy is not
            set, dead lettering is disabled.

            The Cloud Pub/Sub service account associated with this
            subscriptions's parent project (i.e.,
            service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com)
            must have permission to Acknowledge() messages on this
            subscription.
        retry_policy (google.pubsub_v1.types.RetryPolicy):
            A policy that specifies how Pub/Sub retries
            message delivery for this subscription.

            If not set, the default retry policy is applied.
            This generally implies that messages will be
            retried as soon as possible for healthy
            subscribers. RetryPolicy will be triggered on
            NACKs or acknowledgement deadline exceeded
            events for a given message.
        detached (bool):
            Indicates whether the subscription is detached from its
            topic. Detached subscriptions don't receive messages from
            their topic and don't retain any backlog. ``Pull`` and
            ``StreamingPull`` requests will return FAILED_PRECONDITION.
            If the subscription is a push subscription, pushes to the
            endpoint will not be made.
        enable_exactly_once_delivery (bool):
            If true, Pub/Sub provides the following guarantees for the
            delivery of a message with a given value of ``message_id``
            on this subscription:

            -  The message sent to a subscriber is guaranteed not to be
               resent before the message's acknowledgement deadline
               expires.
            -  An acknowledged message will not be resent to a
               subscriber.

            Note that subscribers may still receive multiple copies of a
            message when ``enable_exactly_once_delivery`` is true if the
            message was published multiple times by a publisher client.
            These copies are considered distinct by Pub/Sub and have
            distinct ``message_id`` values.
        topic_message_retention_duration (google.protobuf.duration_pb2.Duration):
            Output only. Indicates the minimum duration for which a
            message is retained after it is published to the
            subscription's topic. If this field is set, messages
            published to the subscription's topic in the last
            ``topic_message_retention_duration`` are always available to
            subscribers. See the ``message_retention_duration`` field in
            ``Topic``. This field is set only in responses from the
            server; it is ignored if it is set in any requests.
        state (google.pubsub_v1.types.Subscription.State):
            Output only. An output-only field indicating
            whether or not the subscription can receive
            messages.
    """

    class State(proto.Enum):
        r"""Possible states for a subscription."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        RESOURCE_ERROR = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    topic = proto.Field(
        proto.STRING,
        number=2,
    )
    push_config = proto.Field(
        proto.MESSAGE,
        number=4,
        message="PushConfig",
    )
    bigquery_config = proto.Field(
        proto.MESSAGE,
        number=18,
        message="BigQueryConfig",
    )
    ack_deadline_seconds = proto.Field(
        proto.INT32,
        number=5,
    )
    retain_acked_messages = proto.Field(
        proto.BOOL,
        number=7,
    )
    message_retention_duration = proto.Field(
        proto.MESSAGE,
        number=8,
        message=duration_pb2.Duration,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    enable_message_ordering = proto.Field(
        proto.BOOL,
        number=10,
    )
    expiration_policy = proto.Field(
        proto.MESSAGE,
        number=11,
        message="ExpirationPolicy",
    )
    filter = proto.Field(
        proto.STRING,
        number=12,
    )
    dead_letter_policy = proto.Field(
        proto.MESSAGE,
        number=13,
        message="DeadLetterPolicy",
    )
    retry_policy = proto.Field(
        proto.MESSAGE,
        number=14,
        message="RetryPolicy",
    )
    detached = proto.Field(
        proto.BOOL,
        number=15,
    )
    enable_exactly_once_delivery = proto.Field(
        proto.BOOL,
        number=16,
    )
    topic_message_retention_duration = proto.Field(
        proto.MESSAGE,
        number=17,
        message=duration_pb2.Duration,
    )
    state = proto.Field(
        proto.ENUM,
        number=19,
        enum=State,
    )


class RetryPolicy(proto.Message):
    r"""A policy that specifies how Cloud Pub/Sub retries message delivery.

    Retry delay will be exponential based on provided minimum and
    maximum backoffs. https://en.wikipedia.org/wiki/Exponential_backoff.

    RetryPolicy will be triggered on NACKs or acknowledgement deadline
    exceeded events for a given message.

    Retry Policy is implemented on a best effort basis. At times, the
    delay between consecutive deliveries may not match the
    configuration. That is, delay can be more or less than configured
    backoff.

    Attributes:
        minimum_backoff (google.protobuf.duration_pb2.Duration):
            The minimum delay between consecutive
            deliveries of a given message. Value should be
            between 0 and 600 seconds. Defaults to 10
            seconds.
        maximum_backoff (google.protobuf.duration_pb2.Duration):
            The maximum delay between consecutive
            deliveries of a given message. Value should be
            between 0 and 600 seconds. Defaults to 600
            seconds.
    """

    minimum_backoff = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )
    maximum_backoff = proto.Field(
        proto.MESSAGE,
        number=2,
        message=duration_pb2.Duration,
    )


class DeadLetterPolicy(proto.Message):
    r"""Dead lettering is done on a best effort basis. The same
    message might be dead lettered multiple times.

    If validation on any of the fields fails at subscription
    creation/updation, the create/update subscription request will
    fail.

    Attributes:
        dead_letter_topic (str):
            The name of the topic to which dead letter messages should
            be published. Format is
            ``projects/{project}/topics/{topic}``.The Cloud Pub/Sub
            service account associated with the enclosing subscription's
            parent project (i.e.,
            service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com)
            must have permission to Publish() to this topic.

            The operation will fail if the topic does not exist. Users
            should ensure that there is a subscription attached to this
            topic since messages published to a topic with no
            subscriptions are lost.
        max_delivery_attempts (int):
            The maximum number of delivery attempts for any message. The
            value must be between 5 and 100.

            The number of delivery attempts is defined as 1 + (the sum
            of number of NACKs and number of times the acknowledgement
            deadline has been exceeded for the message).

            A NACK is any call to ModifyAckDeadline with a 0 deadline.
            Note that client libraries may automatically extend
            ack_deadlines.

            This field will be honored on a best effort basis.

            If this parameter is 0, a default value of 5 is used.
    """

    dead_letter_topic = proto.Field(
        proto.STRING,
        number=1,
    )
    max_delivery_attempts = proto.Field(
        proto.INT32,
        number=2,
    )


class ExpirationPolicy(proto.Message):
    r"""A policy that specifies the conditions for resource
    expiration (i.e., automatic resource deletion).

    Attributes:
        ttl (google.protobuf.duration_pb2.Duration):
            Specifies the "time-to-live" duration for an associated
            resource. The resource expires if it is not active for a
            period of ``ttl``. The definition of "activity" depends on
            the type of the associated resource. The minimum and maximum
            allowed values for ``ttl`` depend on the type of the
            associated resource, as well. If ``ttl`` is not set, the
            associated resource never expires.
    """

    ttl = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )


class PushConfig(proto.Message):
    r"""Configuration for a push delivery endpoint.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        push_endpoint (str):
            A URL locating the endpoint to which messages should be
            pushed. For example, a Webhook endpoint might use
            ``https://example.com/push``.
        attributes (Mapping[str, str]):
            Endpoint configuration attributes that can be used to
            control different aspects of the message delivery.

            The only currently supported attribute is
            ``x-goog-version``, which you can use to change the format
            of the pushed message. This attribute indicates the version
            of the data expected by the endpoint. This controls the
            shape of the pushed message (i.e., its fields and metadata).

            If not present during the ``CreateSubscription`` call, it
            will default to the version of the Pub/Sub API used to make
            such call. If not present in a ``ModifyPushConfig`` call,
            its value will not be changed. ``GetSubscription`` calls
            will always return a valid version, even if the subscription
            was created without this attribute.

            The only supported values for the ``x-goog-version``
            attribute are:

            -  ``v1beta1``: uses the push format defined in the v1beta1
               Pub/Sub API.
            -  ``v1`` or ``v1beta2``: uses the push format defined in
               the v1 Pub/Sub API.

            For example:

            .. raw:: html

                <pre><code>attributes { "x-goog-version": "v1" } </code></pre>
        oidc_token (google.pubsub_v1.types.PushConfig.OidcToken):
            If specified, Pub/Sub will generate and attach an OIDC JWT
            token as an ``Authorization`` header in the HTTP request for
            every pushed message.

            This field is a member of `oneof`_ ``authentication_method``.
    """

    class OidcToken(proto.Message):
        r"""Contains information needed for generating an `OpenID Connect
        token <https://developers.google.com/identity/protocols/OpenIDConnect>`__.

        Attributes:
            service_account_email (str):
                `Service account
                email <https://cloud.google.com/iam/docs/service-accounts>`__
                to be used for generating the OIDC token. The caller (for
                CreateSubscription, UpdateSubscription, and ModifyPushConfig
                RPCs) must have the iam.serviceAccounts.actAs permission for
                the service account.
            audience (str):
                Audience to be used when generating OIDC
                token. The audience claim identifies the
                recipients that the JWT is intended for. The
                audience value is a single case-sensitive
                string. Having multiple values (array) for the
                audience field is not supported. More info about
                the OIDC JWT token audience here:
                https://tools.ietf.org/html/rfc7519#section-4.1.3
                Note: if not specified, the Push endpoint URL
                will be used.
        """

        service_account_email = proto.Field(
            proto.STRING,
            number=1,
        )
        audience = proto.Field(
            proto.STRING,
            number=2,
        )

    push_endpoint = proto.Field(
        proto.STRING,
        number=1,
    )
    attributes = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    oidc_token = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="authentication_method",
        message=OidcToken,
    )


class BigQueryConfig(proto.Message):
    r"""Configuration for a BigQuery subscription.

    Attributes:
        table (str):
            The name of the table to which to write data,
            of the form {projectId}:{datasetId}.{tableId}
        use_topic_schema (bool):
            When true, use the topic's schema as the
            columns to write to in BigQuery, if it exists.
        write_metadata (bool):
            When true, write the subscription name, message_id,
            publish_time, attributes, and ordering_key to additional
            columns in the table. The subscription name, message_id, and
            publish_time fields are put in their own columns while all
            other message properties (other than data) are written to a
            JSON object in the attributes column.
        drop_unknown_fields (bool):
            When true and use_topic_schema is true, any fields that are
            a part of the topic schema that are not part of the BigQuery
            table schema are dropped when writing to BigQuery.
            Otherwise, the schemas must be kept in sync and any messages
            with extra fields are not written and remain in the
            subscription's backlog.
        state (google.pubsub_v1.types.BigQueryConfig.State):
            Output only. An output-only field that
            indicates whether or not the subscription can
            receive messages.
    """

    class State(proto.Enum):
        r"""Possible states for a BigQuery subscription."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        PERMISSION_DENIED = 2
        NOT_FOUND = 3
        SCHEMA_MISMATCH = 4

    table = proto.Field(
        proto.STRING,
        number=1,
    )
    use_topic_schema = proto.Field(
        proto.BOOL,
        number=2,
    )
    write_metadata = proto.Field(
        proto.BOOL,
        number=3,
    )
    drop_unknown_fields = proto.Field(
        proto.BOOL,
        number=4,
    )
    state = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )


class ReceivedMessage(proto.Message):
    r"""A message and its corresponding acknowledgment ID.

    Attributes:
        ack_id (str):
            This ID can be used to acknowledge the
            received message.
        message (google.pubsub_v1.types.PubsubMessage):
            The message.
        delivery_attempt (int):
            The approximate number of times that Cloud Pub/Sub has
            attempted to deliver the associated message to a subscriber.

            More precisely, this is 1 + (number of NACKs) + (number of
            ack_deadline exceeds) for this message.

            A NACK is any call to ModifyAckDeadline with a 0 deadline.
            An ack_deadline exceeds event is whenever a message is not
            acknowledged within ack_deadline. Note that ack_deadline is
            initially Subscription.ackDeadlineSeconds, but may get
            extended automatically by the client library.

            Upon the first delivery of a given message,
            ``delivery_attempt`` will have a value of 1. The value is
            calculated at best effort and is approximate.

            If a DeadLetterPolicy is not set on the subscription, this
            will be 0.
    """

    ack_id = proto.Field(
        proto.STRING,
        number=1,
    )
    message = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PubsubMessage",
    )
    delivery_attempt = proto.Field(
        proto.INT32,
        number=3,
    )


class Snapshot(proto.Message):
    r"""A snapshot resource. Snapshots are used in
    `Seek <https://cloud.google.com/pubsub/docs/replay-overview>`__
    operations, which allow you to manage message acknowledgments in
    bulk. That is, you can set the acknowledgment state of messages in
    an existing subscription to the state captured by a snapshot.

    Attributes:
        name (str):
            The name of the snapshot.
        topic (str):
            The name of the topic from which this
            snapshot is retaining messages.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The snapshot is guaranteed to exist up until this time. A
            newly-created snapshot expires no later than 7 days from the
            time of its creation. Its exact lifetime is determined at
            creation by the existing backlog in the source subscription.
            Specifically, the lifetime of the snapshot is
            ``7 days - (age of oldest unacked message in the subscription)``.
            For example, consider a subscription whose oldest unacked
            message is 3 days old. If a snapshot is created from this
            subscription, the snapshot -- which will always capture this
            3-day-old backlog as long as the snapshot exists -- will
            expire in 4 days. The service will refuse to create a
            snapshot that would expire in less than 1 hour after
            creation.
        labels (Mapping[str, str]):
            See [Creating and managing labels]
            (https://cloud.google.com/pubsub/docs/labels).
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    topic = proto.Field(
        proto.STRING,
        number=2,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
