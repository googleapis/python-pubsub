from opentelemetry.propagators.textmap import Getter
from google.pubsub_v1 import types as gapic_types
import typing


class OTelContextGetter(Getter):
    """Used to extract Open Telemetry Context from message attributes."""

    def get(
        self, carrier: gapic_types.PubsubMessage, key: str
    ) -> typing.Optional[typing.List[str]]:
        return [carrier.attributes["googclient_" + key]]

    def keys(self, carrier: gapic_types.PubsubMessage) -> typing.List[str]:
        return list(carrier.attributes.keys())
