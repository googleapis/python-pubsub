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


__manifest__ = (
    "ListSchemasResponse",
    "ValidateSchemaResponse",
    "ValidateMessageResponse",
)


class ListSchemasResponse(proto.Message):
    r"""Response for the ``ListSchemas`` method.

    Attributes:
        schemas (Sequence[google.pubsub_v1.types.Schema]):
            The resulting schemas.
        next_page_token (str):
            If not empty, indicates that there may be more schemas that
            match the request; this value should be passed in a new
            ``ListSchemasRequest``.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    schemas = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Schema",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ValidateSchemaResponse(proto.Message):
    r"""Response for the ``ValidateSchema`` method. Empty for now."""
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


class ValidateMessageResponse(proto.Message):
    r"""Response for the ``ValidateMessage`` method. Empty for now."""
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore


__all__ = tuple(sorted(__manifest__))
