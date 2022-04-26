# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for StreamingPull
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-pubsub


# [START pubsub_v1_generated_Subscriber_StreamingPull_sync]
from google import pubsub_v1


def sample_streaming_pull():
    # Create a client
    client = pubsub_v1.SubscriberClient()

    # Initialize request argument(s)
    request = pubsub_v1.StreamingPullRequest(
        subscription="subscription_value",
        stream_ack_deadline_seconds=2813,
    )

    # This method expects an iterator which contains
    # 'pubsub_v1.StreamingPullRequest' objects
    # Here we create a generator that yields a single `request` for
    # demonstrative purposes.
    requests = [request]

    def request_generator():
        for request in requests:
            yield request

    # Make the request
    stream = client.streaming_pull(requests=request_generator())

    # Handle the response
    for response in stream:
        print(response)

# [END pubsub_v1_generated_Subscriber_StreamingPull_sync]
