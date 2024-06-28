# Utility class that implements tracerProvider and can be used to test the spans created during development
from typing import Callable
from google.cloud import pubsub_v1
from concurrent import futures
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
# tracer = trace.get_tracer("my.tracer.name")

project_id = "cloud-pubsub-load-tests"
topic_id = "mukund-topic"

publisher = pubsub_v1.PublisherClient(publisher_options=pubsub_v1.types.PublisherOptions(
    enable_open_telemetry_tracing=True,
))
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []

# with tracer.start_as_current_span("tracer provider"):


def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


NUM_MESSAGES_TO_PUBLISH = 1
for i in range(NUM_MESSAGES_TO_PUBLISH):
    data = str(i)
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"Published messages with error handler to {topic_path}.")
