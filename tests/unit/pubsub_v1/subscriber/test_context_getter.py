from google.pubsub_v1 import types as gapic_types
from google.cloud.pubsub_v1.opentelemetry.context_propagation import OTelContextGetter


def test_get():
    message = gapic_types.PubsubMessage(
        data=b"data",
        attributes={
            "non_otel_key": "non_otel_key_value",
            "googclient_traceparent": "traceparent_value",
        },
    )
    val = OTelContextGetter().get(message, "traceparent")
    assert val == ["traceparent_value"]

    val = OTelContextGetter().get(message, "non_existent_key")
    assert val == [""]


def test_keys():
    message = gapic_types.PubsubMessage(
        data=b"data",
        attributes={
            "non_otel_key": "non_otel_key_value",
            "googclient_traceparent": "traceparent_value",
            "googclient_tracestate": "tracestate_value",
        },
    )
    keys = OTelContextGetter().keys(message)
    assert "non_otel_key" in keys
    assert "googclient_traceparent" in keys
    assert "googclient_tracestate" in keys
