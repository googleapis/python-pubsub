from google.pubsub_v1 import types as gapic_types
from opentelemetry import trace
from typing import Optional


class MessageWrapper():
    """
    Wraps Pub/Sub message with additional metadata required for
    Open Telemetry tracing.
    """

    def __init__(self, message: gapic_types.PubsubMessage, create_span: trace.Span):
        self._message = message
        self._create_span = create_span

    def get_message(self) -> gapic_types.PubsubMessage:
        return self._message

    def set_message(self, message: gapic_types.PubsubMessage) -> None:
        self._message = message

    def get_span(self) -> Optional["trace.Span"]:
        return self._create_span

    def __eq__(self, other: "MessageWrapper") -> bool:
        if not isinstance(other, MessageWrapper):
            return False
        return self._message == other._message and self._create_span == other._create_span
