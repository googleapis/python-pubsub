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

from google.cloud import pubsub_v1
import mock
import pytest

import quickstart

PROJECT = os.environ['GCLOUD_PROJECT']
# Must match the dataset listed in quickstart.py
TOPIC_NAME = 'my-new-topic'
TOPIC_PATH = 'projects/{}/topics/{}'.format(PROJECT, TOPIC_NAME)


@pytest.fixture
def temporary_topic():
    """Fixture that ensures the test topic does not exist before the test."""
    publisher = pubsub_v1.PublisherClient()

    try:
        publisher.delete_topic(TOPIC_PATH)
    except Exception:
        pass

    yield


@mock.patch.object(
    pubsub_v1.PublisherClient, 'topic_path', return_value=TOPIC_PATH)
def test_quickstart(unused_topic_path, temporary_topic, capsys):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert TOPIC_NAME in out
