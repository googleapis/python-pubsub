# Copyright 2024, Google LLC All rights reserved.
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

from typing import Optional
from datetime import datetime

from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.propagation import set_span_in_context

from google.cloud.pubsub_v1.open_telemetry.context_propagation import (
    OpenTelemetryContextGetter,
)
from google.pubsub_v1.types import PubsubMessage


class SubscribeOpenTelemetry:
    _OPEN_TELEMETRY_TRACER_NAME: str = "google.cloud.pubsub_v1"
    _OPEN_TELEMETRY_MESSAGING_SYSTEM: str = "gcp_pubsub"

    def __init__(self, message: PubsubMessage):
        self._message: PubsubMessage = message

        # subscribe span will be initialized by the `start_subscribe_span`
        # method.
        self._subscribe_span: Optional[trace.Span] = None

        # subscriber concurrency control span will be initialized by the
        # `start_subscribe_concurrency_control_span` method.
        self._concurrency_control_span: Optional[trace.Span] = None

    def start_subscribe_span(
        self,
        subscription: str,
        exactly_once_enabled: bool,
        ack_id: str,
        delivery_attempt: int,
    ) -> None:
        tracer = trace.get_tracer(self._OPEN_TELEMETRY_TRACER_NAME)
        parent_span_context = TraceContextTextMapPropagator().extract(
            carrier=self._message,
            getter=OpenTelemetryContextGetter(),
        )
        assert len(subscription.split("/")) == 4
        subscription_short_name = subscription.split("/")[3]
        with tracer.start_as_current_span(
            name=f"{subscription_short_name} subscribe",
            context=parent_span_context if parent_span_context else None,
            kind=trace.SpanKind.CONSUMER,
            attributes={
                "messaging.system": self._OPEN_TELEMETRY_MESSAGING_SYSTEM,
                "messaging.destination.name": subscription_short_name,
                "gcp.project_id": subscription.split("/")[1],
                "messaging.message.id": self._message.message_id,
                "messaging.message.body.size": len(self._message.data),
                "messaging.gcp_pubsub.message.ack_id": ack_id,
                "messaging.gcp_pubsub.message.ordering_key": self._message.ordering_key,
                "messaging.gcp_pubsub.message.exactly_once_delivery": exactly_once_enabled,
                "code.function": "_on_response",
                "messaging.gcp_pubsub.message.delivery_attempt": delivery_attempt,
            },
            end_on_exit=False,
        ) as subscribe_span:
            self._subscribe_span = subscribe_span

    def add_subscribe_span_event(self, event: str) -> None:
        assert self._subscribe_span is not None
        self._subscribe_span.add_event(
            name=event,
            attributes={
                "timestamp": str(datetime.now()),
            },
        )

    def end_subscribe_span(self) -> None:
        assert self._subscribe_span is not None
        self._subscribe_span.end()

    def set_subscribe_span_result(self, result: str) -> None:
        assert self._subscribe_span is not None
        self._subscribe_span.set_attribute(
            key="messaging.gcp_pubsub.result",
            value=result,
        )

    def start_subscribe_concurrency_control_span(self) -> None:
        assert self._subscribe_span is not None
        tracer = trace.get_tracer(self._OPEN_TELEMETRY_TRACER_NAME)
        with tracer.start_as_current_span(
            name="subscriber concurrency control",
            kind=trace.SpanKind.INTERNAL,
            context=set_span_in_context(self._subscribe_span),
            end_on_exit=False,
        ) as concurrency_control_span:
            self._concurrency_control_span = concurrency_control_span

    def end_subscribe_concurrency_control_span(self) -> None:
        assert self._concurrency_control_span is not None
        self._concurrency_control_span.end()
