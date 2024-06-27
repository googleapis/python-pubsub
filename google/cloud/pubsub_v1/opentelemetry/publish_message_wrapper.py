from google.pubsub_v1 import types as gapic_types
from opentelemetry import trace
from dataclasses import dataclass, field

from typing import Optional


@dataclass
class PublishMessageWrapper:
    """
    Wraps Pub/Sub message with additional metadata required for
    Open Telemetry tracing.
    """

    message: gapic_types.PubsubMessage
    span: Optional[trace.Span] = field(default=None)
