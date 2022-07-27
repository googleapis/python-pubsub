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


__protobuf__ = proto.module(
    package="google.pubsub.v1",
    manifest={
        "SchemaView",
        "Encoding",
        "Schema",
        "CreateSchemaRequest",
        "GetSchemaRequest",
        "ListSchemasRequest",
        "ListSchemasResponse",
        "DeleteSchemaRequest",
        "ValidateSchemaRequest",
        "ValidateSchemaResponse",
        "ValidateMessageRequest",
        "ValidateMessageResponse",
    },
)


from .requests import (
    CreateSchemaRequest,
    GetSchemaRequest,
    ListSchemasRequest,
    DeleteSchemaRequest,
    ValidateSchemaRequest,
    ValidateMessageRequest,
)

from .responses import (
    ListSchemasResponse,
    ValidateSchemaResponse,
    ValidateMessageResponse,
)


class SchemaView(proto.Enum):
    r"""View of Schema object fields to be returned by GetSchema and
    ListSchemas.
    """
    SCHEMA_VIEW_UNSPECIFIED = 0
    BASIC = 1
    FULL = 2


class Encoding(proto.Enum):
    r"""Possible encoding types for messages."""
    ENCODING_UNSPECIFIED = 0
    JSON = 1
    BINARY = 2


class Schema(proto.Message):
    r"""A schema resource.

    Attributes:
        name (str):
            Required. Name of the schema. Format is
            ``projects/{project}/schemas/{schema}``.
        type_ (google.pubsub_v1.types.Schema.Type):
            The type of the schema definition.
        definition (str):
            The definition of the schema. This should contain a string
            representing the full definition of the schema that is a
            valid schema definition of the type specified in ``type``.
    """

    class Type(proto.Enum):
        r"""Possible schema definition types."""
        TYPE_UNSPECIFIED = 0
        PROTOCOL_BUFFER = 1
        AVRO = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )
    definition = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
