from google.pubsub_v1 import types as gapic_types
from opentelemetry import trace
from dataclasses import dataclass, field


@dataclass
class MessageWrapper:
    """
    Wraps Pub/Sub message with additional metadata required for
    Open Telemetry tracing.
    """

    message: gapic_types.PubsubMessage
    create_span: trace.Span = field(default=None)
