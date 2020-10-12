#!/usr/bin/env python

# Copyright 2019 Google LLC
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
import uuid

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1
import pytest


UUID = uuid.uuid4().hex
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC_ID = "quickstart-sub-test-topic-" + UUID
SUBSCRIPTION_ID = "quickstart-sub-test-topic-sub-" + UUID


@pytest.fixture(scope="module")
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def subscriber_client():
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    subscriber_client.close()


@pytest.fixture(scope="module")
def topic_path(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        topic = publisher_client.create_topic(request={"name": topic_path})
        yield topic.name
    except AlreadyExists:
        yield topic_path

    publisher_client.delete_topic(request={"topic": topic_path})


@pytest.fixture(scope="module")
def subscription_path(subscriber_client, topic_path):
    subscription_path = subscriber_client.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    try:
        subscription = subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
        yield subscription.name
    except AlreadyExists:
        yield subscription_path

    subscriber_client.delete_subscription(request={"subscription": subscription_path})
    subscriber_client.close()


def test_pub(topic_path, capsys):
    import pub

    pub.pub(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert topic_path in out
    assert "Hello, World!" in out


def test_sub(publisher_client, topic_path, subscription_path, capsys):
    publisher_client.publish(topic_path, b"Hello World!")

    import sub

    sub.sub(PROJECT_ID, SUBSCRIPTION_ID, 10)

    out, _ = capsys.readouterr()
    assert f"Listening for messages on {subscription_path}" in out
    assert "Received" in out
    assert "Acknowledged" in out
