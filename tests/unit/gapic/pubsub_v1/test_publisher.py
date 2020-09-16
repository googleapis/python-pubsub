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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.pubsub_v1.services.publisher import PublisherAsyncClient
from google.pubsub_v1.services.publisher import PublisherClient
from google.pubsub_v1.services.publisher import pagers
from google.pubsub_v1.services.publisher import transports
from google.pubsub_v1.types import pubsub


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert PublisherClient._get_default_mtls_endpoint(None) is None
    assert PublisherClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        PublisherClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PublisherClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PublisherClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert PublisherClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [PublisherClient, PublisherAsyncClient])
def test_publisher_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "pubsub.googleapis.com:443"


def test_publisher_client_get_transport_class():
    transport = PublisherClient.get_transport_class()
    assert transport == transports.PublisherGrpcTransport

    transport = PublisherClient.get_transport_class("grpc")
    assert transport == transports.PublisherGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PublisherClient, transports.PublisherGrpcTransport, "grpc"),
        (
            PublisherAsyncClient,
            transports.PublisherGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    PublisherClient, "DEFAULT_ENDPOINT", modify_default_endpoint(PublisherClient)
)
@mock.patch.object(
    PublisherAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PublisherAsyncClient),
)
def test_publisher_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(PublisherClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(PublisherClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (PublisherClient, transports.PublisherGrpcTransport, "grpc", "true"),
        (
            PublisherAsyncClient,
            transports.PublisherGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (PublisherClient, transports.PublisherGrpcTransport, "grpc", "false"),
        (
            PublisherAsyncClient,
            transports.PublisherGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    PublisherClient, "DEFAULT_ENDPOINT", modify_default_endpoint(PublisherClient)
)
@mock.patch.object(
    PublisherAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PublisherAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_publisher_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PublisherClient, transports.PublisherGrpcTransport, "grpc"),
        (
            PublisherAsyncClient,
            transports.PublisherGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_publisher_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PublisherClient, transports.PublisherGrpcTransport, "grpc"),
        (
            PublisherAsyncClient,
            transports.PublisherGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_publisher_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_publisher_client_client_options_from_dict():
    with mock.patch(
        "google.pubsub_v1.services.publisher.transports.PublisherGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = PublisherClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_topic(transport: str = "grpc", request_type=pubsub.Topic):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name="name_value", kms_key_name="kms_key_name_value",
        )

        response = client.create_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.Topic()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_create_topic_from_dict():
    test_create_topic(request_type=dict)


@pytest.mark.asyncio
async def test_create_topic_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.Topic()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Topic(name="name_value", kms_key_name="kms_key_name_value",)
        )

        response = await client.create_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_create_topic_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.Topic()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_topic), "__call__") as call:
        call.return_value = pubsub.Topic()

        client.create_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_topic_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.Topic()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_topic), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Topic())

        await client.create_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_topic_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_topic(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_create_topic_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_topic(
            pubsub.Topic(), name="name_value",
        )


@pytest.mark.asyncio
async def test_create_topic_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Topic())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_topic(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_create_topic_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_topic(
            pubsub.Topic(), name="name_value",
        )


def test_update_topic(transport: str = "grpc", request_type=pubsub.UpdateTopicRequest):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name="name_value", kms_key_name="kms_key_name_value",
        )

        response = client.update_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateTopicRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_update_topic_from_dict():
    test_update_topic(request_type=dict)


@pytest.mark.asyncio
async def test_update_topic_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.UpdateTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Topic(name="name_value", kms_key_name="kms_key_name_value",)
        )

        response = await client.update_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_update_topic_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateTopicRequest()
    request.topic.name = "topic.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_topic), "__call__") as call:
        call.return_value = pubsub.Topic()

        client.update_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic.name=topic.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_topic_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateTopicRequest()
    request.topic.name = "topic.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_topic), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Topic())

        await client.update_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic.name=topic.name/value",) in kw["metadata"]


def test_publish(transport: str = "grpc", request_type=pubsub.PublishRequest):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.publish), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PublishResponse(message_ids=["message_ids_value"],)

        response = client.publish(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.PublishRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.PublishResponse)

    assert response.message_ids == ["message_ids_value"]


def test_publish_from_dict():
    test_publish(request_type=dict)


@pytest.mark.asyncio
async def test_publish_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.PublishRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._client._transport.publish), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.PublishResponse(message_ids=["message_ids_value"],)
        )

        response = await client.publish(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.PublishResponse)

    assert response.message_ids == ["message_ids_value"]


def test_publish_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.PublishRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.publish), "__call__") as call:
        call.return_value = pubsub.PublishResponse()

        client.publish(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_publish_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.PublishRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._client._transport.publish), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.PublishResponse()
        )

        await client.publish(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


def test_publish_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.publish), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PublishResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.publish(
            topic="topic_value", messages=[pubsub.PubsubMessage(data=b"data_blob")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"

        assert args[0].messages == [pubsub.PubsubMessage(data=b"data_blob")]


def test_publish_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.publish(
            pubsub.PublishRequest(),
            topic="topic_value",
            messages=[pubsub.PubsubMessage(data=b"data_blob")],
        )


@pytest.mark.asyncio
async def test_publish_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._client._transport.publish), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PublishResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.PublishResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.publish(
            topic="topic_value", messages=[pubsub.PubsubMessage(data=b"data_blob")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"

        assert args[0].messages == [pubsub.PubsubMessage(data=b"data_blob")]


@pytest.mark.asyncio
async def test_publish_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.publish(
            pubsub.PublishRequest(),
            topic="topic_value",
            messages=[pubsub.PubsubMessage(data=b"data_blob")],
        )


def test_get_topic(transport: str = "grpc", request_type=pubsub.GetTopicRequest):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic(
            name="name_value", kms_key_name="kms_key_name_value",
        )

        response = client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetTopicRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_get_topic_from_dict():
    test_get_topic(request_type=dict)


@pytest.mark.asyncio
async def test_get_topic_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.GetTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Topic(name="name_value", kms_key_name="kms_key_name_value",)
        )

        response = await client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Topic)

    assert response.name == "name_value"

    assert response.kms_key_name == "kms_key_name_value"


def test_get_topic_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetTopicRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_topic), "__call__") as call:
        call.return_value = pubsub.Topic()

        client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_topic_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetTopicRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_topic), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Topic())

        await client.get_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


def test_get_topic_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_topic(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


def test_get_topic_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_topic(
            pubsub.GetTopicRequest(), topic="topic_value",
        )


@pytest.mark.asyncio
async def test_get_topic_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Topic()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Topic())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_topic(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


@pytest.mark.asyncio
async def test_get_topic_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_topic(
            pubsub.GetTopicRequest(), topic="topic_value",
        )


def test_list_topics(transport: str = "grpc", request_type=pubsub.ListTopicsRequest):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_topics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_topics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListTopicsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_topics_from_dict():
    test_list_topics(request_type=dict)


@pytest.mark.asyncio
async def test_list_topics_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_topics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_topics_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_topics), "__call__") as call:
        call.return_value = pubsub.ListTopicsResponse()

        client.list_topics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_topics_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topics), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicsResponse()
        )

        await client.list_topics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


def test_list_topics_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_topics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_topics(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


def test_list_topics_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topics(
            pubsub.ListTopicsRequest(), project="project_value",
        )


@pytest.mark.asyncio
async def test_list_topics_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_topics(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


@pytest.mark.asyncio
async def test_list_topics_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_topics(
            pubsub.ListTopicsRequest(), project="project_value",
        )


def test_list_topics_pager():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_topics), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[pubsub.Topic(), pubsub.Topic(), pubsub.Topic(),],
                next_page_token="abc",
            ),
            pubsub.ListTopicsResponse(topics=[], next_page_token="def",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(),], next_page_token="ghi",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(), pubsub.Topic(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", ""),)),
        )
        pager = client.list_topics(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Topic) for i in results)


def test_list_topics_pages():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_topics), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[pubsub.Topic(), pubsub.Topic(), pubsub.Topic(),],
                next_page_token="abc",
            ),
            pubsub.ListTopicsResponse(topics=[], next_page_token="def",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(),], next_page_token="ghi",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(), pubsub.Topic(),],),
            RuntimeError,
        )
        pages = list(client.list_topics(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_topics_async_pager():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[pubsub.Topic(), pubsub.Topic(), pubsub.Topic(),],
                next_page_token="abc",
            ),
            pubsub.ListTopicsResponse(topics=[], next_page_token="def",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(),], next_page_token="ghi",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(), pubsub.Topic(),],),
            RuntimeError,
        )
        async_pager = await client.list_topics(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, pubsub.Topic) for i in responses)


@pytest.mark.asyncio
async def test_list_topics_async_pages():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicsResponse(
                topics=[pubsub.Topic(), pubsub.Topic(), pubsub.Topic(),],
                next_page_token="abc",
            ),
            pubsub.ListTopicsResponse(topics=[], next_page_token="def",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(),], next_page_token="ghi",),
            pubsub.ListTopicsResponse(topics=[pubsub.Topic(), pubsub.Topic(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_topics(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_topic_subscriptions(
    transport: str = "grpc", request_type=pubsub.ListTopicSubscriptionsRequest
):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSubscriptionsResponse(
            subscriptions=["subscriptions_value"],
            next_page_token="next_page_token_value",
        )

        response = client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListTopicSubscriptionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicSubscriptionsPager)

    assert response.subscriptions == ["subscriptions_value"]

    assert response.next_page_token == "next_page_token_value"


def test_list_topic_subscriptions_from_dict():
    test_list_topic_subscriptions(request_type=dict)


@pytest.mark.asyncio
async def test_list_topic_subscriptions_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicSubscriptionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=["subscriptions_value"],
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicSubscriptionsAsyncPager)

    assert response.subscriptions == ["subscriptions_value"]

    assert response.next_page_token == "next_page_token_value"


def test_list_topic_subscriptions_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSubscriptionsRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        call.return_value = pubsub.ListTopicSubscriptionsResponse()

        client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_topic_subscriptions_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSubscriptionsRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSubscriptionsResponse()
        )

        await client.list_topic_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


def test_list_topic_subscriptions_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSubscriptionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_topic_subscriptions(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


def test_list_topic_subscriptions_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topic_subscriptions(
            pubsub.ListTopicSubscriptionsRequest(), topic="topic_value",
        )


@pytest.mark.asyncio
async def test_list_topic_subscriptions_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSubscriptionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSubscriptionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_topic_subscriptions(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


@pytest.mark.asyncio
async def test_list_topic_subscriptions_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_topic_subscriptions(
            pubsub.ListTopicSubscriptionsRequest(), topic="topic_value",
        )


def test_list_topic_subscriptions_pager():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[], next_page_token="def",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSubscriptionsResponse(subscriptions=[str(), str(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", ""),)),
        )
        pager = client.list_topic_subscriptions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_list_topic_subscriptions_pages():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_subscriptions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[], next_page_token="def",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSubscriptionsResponse(subscriptions=[str(), str(),],),
            RuntimeError,
        )
        pages = list(client.list_topic_subscriptions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_topic_subscriptions_async_pager():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_subscriptions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[], next_page_token="def",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSubscriptionsResponse(subscriptions=[str(), str(),],),
            RuntimeError,
        )
        async_pager = await client.list_topic_subscriptions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_list_topic_subscriptions_async_pages():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_subscriptions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[], next_page_token="def",
            ),
            pubsub.ListTopicSubscriptionsResponse(
                subscriptions=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSubscriptionsResponse(subscriptions=[str(), str(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_topic_subscriptions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_topic_snapshots(
    transport: str = "grpc", request_type=pubsub.ListTopicSnapshotsRequest
):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSnapshotsResponse(
            snapshots=["snapshots_value"], next_page_token="next_page_token_value",
        )

        response = client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListTopicSnapshotsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicSnapshotsPager)

    assert response.snapshots == ["snapshots_value"]

    assert response.next_page_token == "next_page_token_value"


def test_list_topic_snapshots_from_dict():
    test_list_topic_snapshots(request_type=dict)


@pytest.mark.asyncio
async def test_list_topic_snapshots_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.ListTopicSnapshotsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSnapshotsResponse(
                snapshots=["snapshots_value"], next_page_token="next_page_token_value",
            )
        )

        response = await client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTopicSnapshotsAsyncPager)

    assert response.snapshots == ["snapshots_value"]

    assert response.next_page_token == "next_page_token_value"


def test_list_topic_snapshots_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSnapshotsRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_snapshots), "__call__"
    ) as call:
        call.return_value = pubsub.ListTopicSnapshotsResponse()

        client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_topic_snapshots_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListTopicSnapshotsRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_snapshots), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSnapshotsResponse()
        )

        await client.list_topic_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


def test_list_topic_snapshots_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSnapshotsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_topic_snapshots(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


def test_list_topic_snapshots_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_topic_snapshots(
            pubsub.ListTopicSnapshotsRequest(), topic="topic_value",
        )


@pytest.mark.asyncio
async def test_list_topic_snapshots_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListTopicSnapshotsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListTopicSnapshotsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_topic_snapshots(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


@pytest.mark.asyncio
async def test_list_topic_snapshots_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_topic_snapshots(
            pubsub.ListTopicSnapshotsRequest(), topic="topic_value",
        )


def test_list_topic_snapshots_pager():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[str(), str(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", ""),)),
        )
        pager = client.list_topic_snapshots(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_list_topic_snapshots_pages():
    client = PublisherClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_topic_snapshots), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[str(), str(),],),
            RuntimeError,
        )
        pages = list(client.list_topic_snapshots(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_topic_snapshots_async_pager():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_snapshots),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[str(), str(),],),
            RuntimeError,
        )
        async_pager = await client.list_topic_snapshots(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_list_topic_snapshots_async_pages():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_topic_snapshots),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(), str(), str(),], next_page_token="abc",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListTopicSnapshotsResponse(
                snapshots=[str(),], next_page_token="ghi",
            ),
            pubsub.ListTopicSnapshotsResponse(snapshots=[str(), str(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_topic_snapshots(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_topic(transport: str = "grpc", request_type=pubsub.DeleteTopicRequest):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteTopicRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_topic_from_dict():
    test_delete_topic(request_type=dict)


@pytest.mark.asyncio
async def test_delete_topic_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.DeleteTopicRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_topic_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteTopicRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_topic), "__call__") as call:
        call.return_value = None

        client.delete_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_topic_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteTopicRequest()
    request.topic = "topic/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_topic), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_topic(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "topic=topic/value",) in kw["metadata"]


def test_delete_topic_flattened():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_topic), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_topic(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


def test_delete_topic_flattened_error():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_topic(
            pubsub.DeleteTopicRequest(), topic="topic_value",
        )


@pytest.mark.asyncio
async def test_delete_topic_flattened_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_topic), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_topic(topic="topic_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].topic == "topic_value"


@pytest.mark.asyncio
async def test_delete_topic_flattened_error_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_topic(
            pubsub.DeleteTopicRequest(), topic="topic_value",
        )


def test_detach_subscription(
    transport: str = "grpc", request_type=pubsub.DetachSubscriptionRequest
):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.detach_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.DetachSubscriptionResponse()

        response = client.detach_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DetachSubscriptionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.DetachSubscriptionResponse)


def test_detach_subscription_from_dict():
    test_detach_subscription(request_type=dict)


@pytest.mark.asyncio
async def test_detach_subscription_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = pubsub.DetachSubscriptionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.detach_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.DetachSubscriptionResponse()
        )

        response = await client.detach_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.DetachSubscriptionResponse)


def test_detach_subscription_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DetachSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.detach_subscription), "__call__"
    ) as call:
        call.return_value = pubsub.DetachSubscriptionResponse()

        client.detach_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_detach_subscription_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DetachSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.detach_subscription), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.DetachSubscriptionResponse()
        )

        await client.detach_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PublisherClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PublisherClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PublisherClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = PublisherClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PublisherGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.PublisherGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.PublisherGrpcTransport, transports.PublisherGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.PublisherGrpcTransport,)


def test_publisher_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.PublisherTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_publisher_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.pubsub_v1.services.publisher.transports.PublisherTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PublisherTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_topic",
        "update_topic",
        "publish",
        "get_topic",
        "list_topics",
        "list_topic_subscriptions",
        "list_topic_snapshots",
        "delete_topic",
        "detach_subscription",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_publisher_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.pubsub_v1.services.publisher.transports.PublisherTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.PublisherTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


def test_publisher_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.pubsub_v1.services.publisher.transports.PublisherTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.PublisherTransport()
        adc.assert_called_once()


def test_publisher_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        PublisherClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id=None,
        )


def test_publisher_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.PublisherGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


def test_publisher_host_no_port():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com"
        ),
    )
    assert client._transport._host == "pubsub.googleapis.com:443"


def test_publisher_host_with_port():
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "pubsub.googleapis.com:8000"


def test_publisher_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.PublisherGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_publisher_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.PublisherGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [transports.PublisherGrpcTransport, transports.PublisherGrpcAsyncIOTransport],
)
def test_publisher_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/pubsub",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.PublisherGrpcTransport, transports.PublisherGrpcAsyncIOTransport],
)
def test_publisher_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/pubsub",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_topic_path():
    project = "squid"
    topic = "clam"

    expected = "projects/{project}/topics/{topic}".format(project=project, topic=topic,)
    actual = PublisherClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "whelk",
        "topic": "octopus",
    }
    path = PublisherClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = PublisherClient.parse_topic_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.PublisherTransport, "_prep_wrapped_messages"
    ) as prep:
        client = PublisherClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.PublisherTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = PublisherClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_set_iam_policy(transport: str = "grpc"):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = PublisherClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = PublisherAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse(permissions=["permissions_value"],)
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = PublisherAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = PublisherClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()
