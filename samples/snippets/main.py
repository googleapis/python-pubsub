from google.cloud import pubsub_v1
pub_sub_client = pubsub_v1.PublisherClient()

if __name__ == '__main__':
    result = pub_sub_client.publish("projects/annaco-python-lib-test/topics/annaco-python-lib-test-topic", bytes("Some message here!", "utf8")).result()