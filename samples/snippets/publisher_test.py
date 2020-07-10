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

from gcp_devrel.testing import eventually_consistent
from google.cloud import pubsub_v1
import mock
import pytest

import publisher

PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'publisher-test-topic'


@pytest.fixture
def client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture
def topic(client):
    topic_path = client.topic_path(PROJECT, TOPIC)

    try:
        client.delete_topic(topic_path)
    except Exception:
        pass

    client.create_topic(topic_path)

    yield topic_path


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError('sigil')
        else:
            real_sleep(period)

    return mock.patch('time.sleep', new=new_sleep)


def test_list(client, topic, capsys):
    @eventually_consistent.call
    def _():
        publisher.list_topics(PROJECT)
        out, _ = capsys.readouterr()
        assert topic in out


def test_create(client):
    topic_path = client.topic_path(PROJECT, TOPIC)
    try:
        client.delete_topic(topic_path)
    except Exception:
        pass

    publisher.create_topic(PROJECT, TOPIC)

    @eventually_consistent.call
    def _():
        assert client.get_topic(topic_path)


def test_delete(client, topic):
    publisher.delete_topic(PROJECT, TOPIC)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            client.get_topic(client.topic_path(PROJECT, TOPIC))


def test_publish(topic, capsys):
    publisher.publish_messages(PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert 'Published' in out


def test_publish_with_custom_attributes(topic, capsys):
    publisher.publish_messages_with_custom_attributes(PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert 'Published' in out


def test_publish_with_batch_settings(topic, capsys):
    publisher.publish_messages_with_batch_settings(PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert 'Published' in out


def test_publish_with_error_handler(topic, capsys):

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            publisher.publish_messages_with_error_handler(
                PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert 'Published' in out


def test_publish_with_futures(topic, capsys):
    publisher.publish_messages_with_futures(PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert 'Published' in out
