import mock
import json
import sys
import types as stdlib_types
import pytest
from importlib import reload

from google.auth import credentials
from google.api_core import bidi
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import opentelemetry_tracing

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

TEST_SPAN_NAME = "foo"

TEST_SPAN_ATTRIBUTES = {"foo": "bar"}

TEST_PARENT_SPAN_CONTEXT = {
    "trace_id": 253178191101418583724305005272987492287,
    "span_id": 17783848543062801337,
    "is_remote": False,
    "trace_flags": 1,
    "trace_state": {},
}


def _create_publisher():
    creds = mock.Mock(spec=credentials)
    return publisher.Client(credentials=creds)


def _create_subscriber():
    creds = mock.Mock(spec=credentials)
    return subscriber.Client(credentials=creds)


def _simulate_pubsub_session():
    test_publisher = _create_publisher()
    test_subscriber = _create_subscriber()
    test_subscriber.subscribe("test_topic", callback=mock.sentinel.callback)
    test_publisher.publish("test_topic", b"foobar")


def _convert_context_to_dict(context):
    return {
        "trace_id": context.trace_id,
        "span_id": context.span_id,
        "is_remote": context.is_remote,
        "trace_flags": context.trace_flags,
        "trace_state": context.trace_state,
    }

def test_not_installed():
    tmp_opentelemetry = sys.modules["opentelemetry"]
    sys.modules["opentelemetry"] = None
    reload(opentelemetry_tracing)
    with opentelemetry_tracing.create_span("OpenTelemetry not installed") as span:
        assert span is None
    sys.modules["opentelemetry"] = tmp_opentelemetry
    reload(opentelemetry_tracing)

@pytest.fixture
def setup():
    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = SimpleExportSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    yield memory_exporter

def test_span_creation(setup):
    with opentelemetry_tracing.create_span(
            TEST_SPAN_NAME,
            attributes=TEST_SPAN_ATTRIBUTES,
            parent=TEST_PARENT_SPAN_CONTEXT,
        ) as span:
            if span is None:
                span_list = setup.get_finished_spans()
                assert len(span_list) == 1
                span = span_list[0]
            assert span.name == TEST_SPAN_NAME
            assert span.attributes == TEST_SPAN_ATTRIBUTES
            assert span.parent.trace_id == TEST_PARENT_SPAN_CONTEXT["trace_id"]

def test_parent_span_linking(setup):
    with opentelemetry_tracing.create_span("Parent") as parent_span:
            parent_span_context = _convert_context_to_dict(parent_span.get_context())
            with opentelemetry_tracing.create_span(
                "Child", parent=parent_span_context
            ) as child_span:
                child_span_context = child_span.get_context()
                assert parent_span_context["trace_id"] == child_span_context.trace_id

def test_trace_call(setup):
    _simulate_pubsub_session()
    span_list = setup.get_finished_spans()
    assert len(span_list) == 1