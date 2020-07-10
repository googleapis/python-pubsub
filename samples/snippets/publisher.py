#!/usr/bin/env python

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

"""This application demonstrates how to perform basic operations on topics
with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse
import time

from google.cloud import pubsub_v1


def list_topics(project):
    """Lists all Pub/Sub topics in the given project."""
    # [START pubsub_list_topics]
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project)

    for topic in publisher.list_topics(project_path):
        print(topic)
    # [END pubsub_list_topics]


def create_topic(project, topic_name):
    """Create a new Pub/Sub topic."""
    # [START pubsub_create_topic]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    topic = publisher.create_topic(topic_path)

    print('Topic created: {}'.format(topic))
    # [END pubsub_create_topic]


def delete_topic(project, topic_name):
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_topic]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    publisher.delete_topic(topic_path)

    print('Topic deleted: {}'.format(topic_path))
    # [END pubsub_delete_topic]


def publish_messages(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]


def publish_messages_with_custom_attributes(project, topic_name):
    """Publishes multiple messages with custom attributes
    to a Pub/Sub topic."""
    # [START pubsub_publish_custom_attributes]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # Add two attributes, origin and username, to the message
        publisher.publish(
            topic_path, data, origin='python-sample', username='gcp')

    print('Published messages with custom attributes.')
    # [END pubsub_publish_custom_attributes]


def publish_messages_with_futures(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic and prints their
    message IDs."""
    # [START pubsub_publisher_concurrency_control]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    # When you publish a message, the client returns a Future. This Future
    # can be used to track when the message is published.
    futures = []

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        message_future = publisher.publish(topic_path, data=data)
        futures.append(message_future)

    print('Published message IDs:')
    for future in futures:
        # result() blocks until the message is published.
        print(future.result())
    # [END pubsub_publisher_concurrency_control]


def publish_messages_with_error_handler(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    # [START pubsub_publish_messages_error_handler]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    def callback(message_future):
        # When timeout is unspecified, the exception method waits indefinitely.
        if message_future.exception(timeout=30):
            print('Publishing message on {} threw an Exception {}.'.format(
                topic_name, message_future.exception()))
        else:
            print(message_future.result())

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # When you publish a message, the client returns a Future.
        message_future = publisher.publish(topic_path, data=data)
        message_future.add_done_callback(callback)

    print('Published message IDs:')

    # We must keep the main thread from exiting to allow it to process
    # messages in the background.
    while True:
        time.sleep(60)
    # [END pubsub_publish_messages_error_handler]


def publish_messages_with_batch_settings(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with batch settings."""
    # [START pubsub_publisher_batch_settings]
    # Configure the batch to publish once there is one kilobyte of data or
    # 1 second has passed.
    batch_settings = pubsub_v1.types.BatchSettings(
        max_bytes=1024,  # One kilobyte
        max_latency=1,  # One second
    )
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')
    # [END pubsub_publisher_batch_settings]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help=list_topics.__doc__)

    create_parser = subparsers.add_parser('create', help=create_topic.__doc__)
    create_parser.add_argument('topic_name')

    delete_parser = subparsers.add_parser('delete', help=delete_topic.__doc__)
    delete_parser.add_argument('topic_name')

    publish_parser = subparsers.add_parser(
        'publish', help=publish_messages.__doc__)
    publish_parser.add_argument('topic_name')

    publish_with_custom_attributes_parser = subparsers.add_parser(
        'publish-with-custom-attributes',
        help=publish_messages_with_custom_attributes.__doc__)
    publish_with_custom_attributes_parser.add_argument('topic_name')

    publish_with_futures_parser = subparsers.add_parser(
        'publish-with-futures',
        help=publish_messages_with_futures.__doc__)
    publish_with_futures_parser.add_argument('topic_name')

    publish_with_error_handler_parser = subparsers.add_parser(
        'publish-with-error-handler',
        help=publish_messages_with_error_handler.__doc__)
    publish_with_error_handler_parser.add_argument('topic_name')

    publish_with_batch_settings_parser = subparsers.add_parser(
        'publish-with-batch-settings',
        help=publish_messages_with_batch_settings.__doc__)
    publish_with_batch_settings_parser.add_argument('topic_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_topics(args.project)
    elif args.command == 'create':
        create_topic(args.project, args.topic_name)
    elif args.command == 'delete':
        delete_topic(args.project, args.topic_name)
    elif args.command == 'publish':
        publish_messages(args.project, args.topic_name)
    elif args.command == 'publish-with-custom-attributes':
        publish_messages_with_custom_attributes(args.project, args.topic_name)
    elif args.command == 'publish-with-futures':
        publish_messages_with_futures(args.project, args.topic_name)
    elif args.command == 'publish-with-error-handler':
        publish_messages_with_error_handler(args.project, args.topic_name)
    elif args.command == 'publish-with-batch-settings':
        publish_messages_with_batch_settings(args.project, args.topic_name)
