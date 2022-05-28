from google.cloud import pubsub_v1 as pubsub
import time

if __name__ == "__main__":  # noqa
    subscriber = pubsub.SubscriberClient()
    flow_control = pubsub.types.FlowControl(max_messages=200)
    sub_path = subscriber.subscription_path(
        "annaco-python-lib-test", "test-subscription"
    )
    publish_topic_name = "annaco-python-lib-test-topic"
    publish_topic_path = subscriber.topic_path(
        "annaco-python-lib-test", publish_topic_name
    )

    def callback(message: pubsub.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        time.sleep(400)
        message.ack()

    future = subscriber.subscribe(sub_path, callback, flow_control)

    print(f"Listening for messages on {sub_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            future.result()
        except TimeoutError:
            future.cancel()  # Trigger the shutdown.
            future.result()  # Block until the shutdown is complete.
