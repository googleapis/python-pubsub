# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import uuid

import backoff
from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
import mock
import pytest

import publisher

UUID = uuid.uuid4().hex
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC_ID = "publisher-test-topic-" + UUID
SUBSCRIPTION_ID = "publisher-test-subscription-" + UUID
# Allow 60s for tests to finish.
MAX_TIME = 60


@pytest.fixture(scope="module")
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def subscriber_client():
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    # Close the subscriber client properly during teardown.
    subscriber_client.close()


@pytest.fixture(scope="module")
def topic_path(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
    except NotFound:
        topic = publisher_client.create_topic(request={"name": topic_path})

    yield topic.name

    try:
        publisher_client.delete_topic(request={"topic": topic.name})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def subscription_path(subscriber_client, topic_path):
    subscription_path = subscriber_client.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    subscription = subscriber_client.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )
    yield subscription.name

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError("sigil")
        else:
            real_sleep(period)

    return mock.patch("time.sleep", new=new_sleep)


def test_create(publisher_client, capsys):
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path}" in out


def test_list(topic_path, capsys):
    publisher.list_topics(PROJECT_ID)
    out, _ = capsys.readouterr()

    assert topic_path in out


def test_publish(topic_path, capsys):
    publisher.publish_messages(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages to {topic_path}." in out


def test_publish_with_custom_attributes(topic_path, capsys):
    publisher.publish_messages_with_custom_attributes(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with custom attributes to {topic_path}." in out


def test_publish_with_batch_settings(topic_path, capsys):
    publisher.publish_messages_with_batch_settings(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with batch settings to {topic_path}." in out


def test_publish_with_retry_settings(topic_path, capsys):
    publisher.publish_messages_with_retry_settings(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with retry settings to {topic_path}." in out


def test_publish_with_error_handler(topic_path, capsys):
    publisher.publish_messages_with_error_handler(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with error handler to {topic_path}." in out


def test_publish_with_ordering_keys(topic_path, capsys):
    publisher.publish_with_ordering_keys(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with ordering keys to {topic_path}." in out


def test_resume_publish_with_error_handler(topic_path, capsys):
    publisher.resume_publish_with_ordering_keys(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Resumed publishing messages with ordering keys to {topic_path}." in out


def test_detach_subscription(subscription_path, capsys):
    publisher.detach_subscription(PROJECT_ID, SUBSCRIPTION_ID)

    out, _ = capsys.readouterr()
    assert f"{subscription_path} is detached." in out


def test_delete(publisher_client):
    publisher.delete_topic(PROJECT_ID, TOPIC_ID)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=MAX_TIME)
    def eventually_consistent_test():
        with pytest.raises(Exception):
            publisher_client.get_topic(
                request={"topic": publisher_client.topic_path(PROJECT_ID, TOPIC_ID)}
            )

    eventually_consistent_test()
