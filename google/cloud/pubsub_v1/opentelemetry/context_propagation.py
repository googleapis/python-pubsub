from opentelemetry.propagators.textmap import Getter
from google.pubsub_v1 import types as gapic_types
import typing


class OTelContextGetter(Getter):
    """TODO:Add docstring later"""

    def get(
        self, carrier: gapic_types.PubsubMessage, key: str
    ) -> typing.Optional[typing.List[str]]:
        print(type(carrier))
        return carrier.attributes[key]

    def keys(self, carrier: gapic_types.PubsubMessage) -> typing.List[str]:
        return carrier.attributes.keys()
