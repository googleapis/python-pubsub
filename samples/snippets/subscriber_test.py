# Copyright 2019 Google Inc. All Rights Reserved.
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
from gcp_devrel.testing.flaky import flaky
from google.cloud import pubsub_v1
import google.api_core.exceptions
import mock
import pytest

import subscriber

PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'subscription-test-topic'
SUBSCRIPTION = 'subscription-test-subscription'
SUBSCRIPTION_SYNC1 = 'subscription-test-subscription-sync1'
SUBSCRIPTION_SYNC2 = 'subscription-test-subscription-sync2'
ENDPOINT = 'https://{}.appspot.com/push'.format(PROJECT)
NEW_ENDPOINT = 'https://{}.appspot.com/push2'.format(PROJECT)


@pytest.fixture(scope='module')
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope='module')
def topic(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.delete_topic(topic_path)
    except Exception:
        pass

    publisher_client.create_topic(topic_path)

    yield topic_path


@pytest.fixture(scope='module')
def subscriber_client():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture
def subscription(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)

    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    try:
        subscriber_client.create_subscription(subscription_path, topic=topic)
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield subscription_path


@pytest.fixture
def subscription_sync1(subscriber_client, topic):
    subscription_sync_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_SYNC1)

    try:
        subscriber_client.delete_subscription(subscription_sync_path)
    except Exception:
        pass

    subscriber_client.create_subscription(subscription_sync_path, topic=topic)

    yield subscription_sync_path


@pytest.fixture
def subscription_sync2(subscriber_client, topic):
    subscription_sync_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_SYNC2)

    try:
        subscriber_client.delete_subscription(subscription_sync_path)
    except Exception:
        pass

    subscriber_client.create_subscription(subscription_sync_path, topic=topic)

    yield subscription_sync_path


def test_list_in_topic(subscription, capsys):
    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions_in_topic(PROJECT, TOPIC)
        out, _ = capsys.readouterr()
        assert subscription in out


def test_list_in_project(subscription, capsys):
    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions_in_project(PROJECT)
        out, _ = capsys.readouterr()
        assert subscription in out


def test_create(subscriber_client):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)
    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    subscriber.create_subscription(PROJECT, TOPIC, SUBSCRIPTION)

    @eventually_consistent.call
    def _():
        assert subscriber_client.get_subscription(subscription_path)


def test_create_push(subscriber_client):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)
    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    subscriber.create_push_subscription(PROJECT, TOPIC, SUBSCRIPTION, ENDPOINT)

    @eventually_consistent.call
    def _():
        assert subscriber_client.get_subscription(subscription_path)


def test_delete(subscriber_client, subscription):
    subscriber.delete_subscription(PROJECT, SUBSCRIPTION)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            subscriber_client.get_subscription(subscription)


def test_update(subscriber_client, subscription, capsys):
    subscriber.update_subscription(PROJECT, SUBSCRIPTION, NEW_ENDPOINT)

    out, _ = capsys.readouterr()
    assert 'Subscription updated' in out


def _publish_messages(publisher_client, topic):
    for n in range(5):
        data = u'Message {}'.format(n).encode('utf-8')
        future = publisher_client.publish(
            topic, data=data)
        future.result()


def _publish_messages_with_custom_attributes(publisher_client, topic):
    data = u'Test message'.encode('utf-8')
    future = publisher_client.publish(topic, data=data, origin='python-sample')
    future.result()


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError('sigil')
        else:
            real_sleep(period)

    return mock.patch('time.sleep', new=new_sleep)


@flaky
def test_receive(publisher_client, topic, subscription, capsys):
    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages(PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription in out
    assert 'Message 1' in out


def test_receive_synchronously(
        publisher_client, topic, subscription_sync1, capsys):
    _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull(PROJECT, SUBSCRIPTION_SYNC1)

    out, _ = capsys.readouterr()
    assert 'Done.' in out


def test_receive_synchronously_with_lease(
        publisher_client, topic, subscription_sync2, capsys):
    _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull_with_lease_management(
        PROJECT, SUBSCRIPTION_SYNC2)

    out, _ = capsys.readouterr()
    assert 'Done.' in out


def test_receive_with_custom_attributes(
        publisher_client, topic, subscription, capsys):
    _publish_messages_with_custom_attributes(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages_with_custom_attributes(
                PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert 'Test message' in out
    assert 'origin' in out
    assert 'python-sample' in out


def test_receive_with_flow_control(
        publisher_client, topic, subscription, capsys):
    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages_with_flow_control(
                PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription in out
    assert 'Message 1' in out
