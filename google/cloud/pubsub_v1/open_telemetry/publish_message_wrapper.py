import sys
from datetime import datetime
import warnings
from typing import Optional

from google.pubsub_v1 import types as gapic_types
from opentelemetry import trace
from opentelemetry.trace.propagation import set_span_in_context
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from google.cloud.pubsub_v1.open_telemetry.context_propagation import (
    OpenTelemetryContextSetter,
)


class PublishMessageWrapper:
    _OPEN_TELEMETRY_TRACER_NAME: str = "google.cloud.pubsub_v1.publisher"
    _OPEN_TELEMETRY_MESSAGING_SYSTEM: str = "gcp_pubsub"
    _OPEN_TELEMETRY_PUBLISHER_BATCHING = "publisher batching"

    _PUBLISH_START_EVENT: str = "publish start"
    _PUBLISH_FLOW_CONTROL: str = "publisher flow control"

    def __init__(self, message: gapic_types.PubsubMessage):
        self._message: gapic_types.PubsubMessage = message

    @property
    def message(self):
        return self._message

    @message.setter  # type: ignore[no-redef]  # resetting message value is intentional here
    def message(self, message: gapic_types.PubsubMessage):
        self._message = message

    @property
    def create_span(self):
        return self._create_span

    def __eq__(self, other):  # pragma: NO COVER
        """Used for pytest asserts to compare two PublishMessageWrapper objects with the same message."""
        if isinstance(self, other.__class__):
            return self.message == other.message
        return False

    def start_create_span(self, topic: str, ordering_key: str) -> None:
        tracer = trace.get_tracer(self._OPEN_TELEMETRY_TRACER_NAME)
        with tracer.start_as_current_span(
            name=f"{topic} create",
            attributes={
                "messaging.system": self._OPEN_TELEMETRY_MESSAGING_SYSTEM,
                "messaging.destination.name": topic,
                "code.function": "google.cloud.pubsub.PublisherClient.publish",
                "messaging.gcp_pubsub.message.ordering_key": ordering_key,
                "messaging.operation": "create",
                "gcp.project_id": topic.split("/")[1],
                "messaging.message.body.size": sys.getsizeof(self._message.data),
            },
            kind=trace.SpanKind.PRODUCER,
            end_on_exit=False,
        ) as create_span:
            create_span.add_event(
                name=self._PUBLISH_START_EVENT,
                attributes={
                    "timestamp": str(datetime.now()),
                },
            )
            self._create_span: trace.Span = create_span
            TraceContextTextMapPropagator().inject(
                carrier=self._message,
                setter=OpenTelemetryContextSetter(),
            )

    def end_create_span(self, exc: Optional[BaseException] = None) -> None:
        if self._create_span is None:  # pragma: NO COVER
            warnings.warn(
                message="publish create span is None. Hence, not ending it",
                category=RuntimeWarning,
            )
            return
        if exc:
            self._create_span.record_exception(exception=exc)
            self._create_span.set_status(
                trace.Status(status_code=trace.StatusCode.ERROR)
            )
        self._create_span.end()

    def start_publisher_flow_control_span(self) -> None:
        tracer = trace.get_tracer(self._OPEN_TELEMETRY_TRACER_NAME)
        if self._create_span is None:  # pragma: NO COVER
            warnings.warn(
                message="publish create span is None. Hence, not starting publish flow control span",
                category=RuntimeWarning,
            )
            return
        with tracer.start_as_current_span(
            name=self._PUBLISH_FLOW_CONTROL,
            kind=trace.SpanKind.INTERNAL,
            context=set_span_in_context(self._create_span),
            end_on_exit=False,
        ) as flow_control_span:
            self._flow_control_span: trace.Span = flow_control_span

    def end_publisher_flow_control_span(
        self, exc: Optional[BaseException] = None
    ) -> None:
        if self._flow_control_span is None:  # pragma: NO COVER
            warnings.warn(
                message="publish flow control span is None. Hence, not ending it",
                category=RuntimeWarning,
            )
            return
        if exc:
            self._flow_control_span.record_exception(exception=exc)
            self._flow_control_span.set_status(
                trace.Status(status_code=trace.StatusCode.ERROR)
            )
        self._flow_control_span.end()

    def start_publisher_batching_span(self) -> None:
        if self._create_span is None:  # pragma: NO COVER
            warnings.warn(
                message="publish create span is None. Hence, not starting publisher batching span",
                category=RuntimeWarning,
            )
            return
        tracer = trace.get_tracer(self._OPEN_TELEMETRY_TRACER_NAME)
        with tracer.start_as_current_span(
            name=self._OPEN_TELEMETRY_PUBLISHER_BATCHING,
            kind=trace.SpanKind.INTERNAL,
            context=set_span_in_context(self._create_span),
            end_on_exit=False,
        ) as batching_span:
            self._batching_span = batching_span

    def end_publisher_batching_span(self, exc: Optional[BaseException] = None) -> None:
        if self._batching_span is None:  # pragma: NO COVER
            warnings.warn(
                message="publisher batching span is None. Hence, not ending it",
                category=RuntimeWarning,
            )
            return
        if exc:
            self._batching_span.record_exception(exception=exc)
            self._batching_span.set_status(
                trace.Status(status_code=trace.StatusCode.ERROR)
            )
        self._batching_span.end()
