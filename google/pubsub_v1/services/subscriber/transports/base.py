# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import abc
import typing

from google import auth
from google.api_core import exceptions  # type: ignore
from google.auth import credentials  # type: ignore

from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.pubsub_v1.types import pubsub


class SubscriberTransport(abc.ABC):
    """Abstract transport class for Subscriber."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    def __init__(
        self,
        *,
        host: str = "pubsub.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    @property
    def create_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.Subscription],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def get_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.GetSubscriptionRequest],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def update_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.UpdateSubscriptionRequest],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def list_subscriptions(
        self,
    ) -> typing.Callable[
        [pubsub.ListSubscriptionsRequest],
        typing.Union[
            pubsub.ListSubscriptionsResponse,
            typing.Awaitable[pubsub.ListSubscriptionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.DeleteSubscriptionRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def modify_ack_deadline(
        self,
    ) -> typing.Callable[
        [pubsub.ModifyAckDeadlineRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def acknowledge(
        self,
    ) -> typing.Callable[
        [pubsub.AcknowledgeRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def pull(
        self,
    ) -> typing.Callable[
        [pubsub.PullRequest],
        typing.Union[pubsub.PullResponse, typing.Awaitable[pubsub.PullResponse]],
    ]:
        raise NotImplementedError()

    @property
    def streaming_pull(
        self,
    ) -> typing.Callable[
        [pubsub.StreamingPullRequest],
        typing.Union[
            pubsub.StreamingPullResponse, typing.Awaitable[pubsub.StreamingPullResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def modify_push_config(
        self,
    ) -> typing.Callable[
        [pubsub.ModifyPushConfigRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.GetSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def list_snapshots(
        self,
    ) -> typing.Callable[
        [pubsub.ListSnapshotsRequest],
        typing.Union[
            pubsub.ListSnapshotsResponse, typing.Awaitable[pubsub.ListSnapshotsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.CreateSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def update_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.UpdateSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def delete_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.DeleteSnapshotRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def seek(
        self,
    ) -> typing.Callable[
        [pubsub.SeekRequest],
        typing.Union[pubsub.SeekResponse, typing.Awaitable[pubsub.SeekResponse]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("SubscriberTransport",)
