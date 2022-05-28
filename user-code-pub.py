from google.cloud import pubsub_v1 as pubsub


if __name__ == "__main__":  # noqa
    publisher = pubsub.PublisherClient()
    publish_topic_name = "annaco-python-lib-test-topic"
    publish_topic_path = publisher.topic_path(
        "annaco-python-lib-test", publish_topic_name
    )

    for i in range(100):
        future = publisher.publish(publish_topic_path, str(i).encode("utf-8"))
        message_id = future.result()
        print("published: " + str(message_id) + " to " + publish_topic_path)
