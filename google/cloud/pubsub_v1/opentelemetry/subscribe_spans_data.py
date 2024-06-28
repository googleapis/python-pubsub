from dataclasses import dataclass
from typing import Optional

from opentelemetry.trace.span import Span


@dataclass
class OpenTelemetryData:
    """
    This class is for internal use by the library only.
    Contains Open Telmetry data associated with a
    google.cloud.pubsub_v1.subscriber.message.Message. Specifically it contains
    the subscriber side spans associated with the message.

    This is so that the subsriber side spans can be ended by the library
    after receiving the message back via an ack(), ack_with_response(), nack().
    """

    subscribe_span: Optional[Span] = None
    concurrrency_control_span: Optional[Span] = None
    scheduler_span: Optional[Span] = None
    process_span: Optional[Span] = None
