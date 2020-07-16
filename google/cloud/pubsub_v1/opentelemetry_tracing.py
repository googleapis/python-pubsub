# Copyright 2020, Google LLC All rights reserved.
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

import logging
from contextlib import contextmanager

from google.api_core.exceptions import GoogleAPICallError

_LOGGER = logging.getLogger(__name__)

try:
    from opentelemetry import trace
    from opentelemetry import propagators
    from opentelemetry.trace import SpanContext
    from opentelemetry.trace import get_current_span
    from opentelemetry.trace import set_span_in_context
    from opentelemetry.trace.status import Status
    from opentelemetry.instrumentation.utils import http_status_to_canonical_code

    USE_OPENTELEMETRY = True
except ImportError:
    _LOGGER.info(
        "This service supports OpenTelemetry, but OpenTelemetry could"
        "not be imported. To use OpenTelemetry, please install the"
        "opentelemetry-api and opentelemetry-instrumentation"
        "pip modules. See also"
        "https://opentelemetry-python.readthedocs.io/en/stable/getting-started.html"
    )
    USE_OPENTELEMETRY = False


@contextmanager
def create_span(span_name, attributes=None, parent=None):
    """ Create a new OpenTelemetry span

    Args:
        span_name (str): the name of the new span
        attributes Optional[dict]: A dictionary
            containing all attributes to add to a span. Defaults to None.
        parent Optional[dict]: A dictionary
            containing the attributes of a parent span's span
            context. Defaults to None.

    Yields:
        [opentelemetry.trace.Span]: The newly created span, or None if
            OpenTelemetry could not be imported
    """

    # OpenTelemetry could not be imported.
    if not USE_OPENTELEMETRY:
        yield None
        return

    tracer = trace.get_tracer(__name__)

    if parent is not None:
        # Form the parent's context from the parent dict provided
        try:
            parent_span_context = SpanContext(**parent)
        except TypeError:
            _LOGGER.warning(
                "A parent span was provided but it could not be"
                "converted into a SpanContext. Ensure that the"
                "parent is a mapping with at least a trace_id, span_id"
                "and is_remote keys."
            )
            parent_span_context = None
    else:
        parent_span_context = None

    # Create a new span and yield it
    with tracer.start_as_current_span(
        span_name, attributes=attributes, parent=parent_span_context
    ) as span:
        try:
            yield span
        except GoogleAPICallError as error:
            if error.code is not None:
                span.set_status(Status(http_status_to_canonical_code(error.code)))
            raise
