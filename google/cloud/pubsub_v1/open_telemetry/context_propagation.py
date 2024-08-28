from opentelemetry.propagators.textmap import Setter
from google.pubsub_v1 import types as gapic_types


class OpenTelemetryContextSetter(Setter):
    """
    Used by Open Telemetry for context propagation.
    """

    def set(self, carrier: gapic_types.PubsubMessage, key: str, value: str):
        """
        Injects trace context into Pub/Sub message attributes with
        "googclient_" prefix.
        """
        carrier.attributes["googclient_" + key] = value
