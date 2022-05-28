import shutil
import argparse
import time
import json
import subprocess, shlex
from pathlib import Path
import concurrent.futures
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import exceptions as sub_exceptions


def run_command(cmd_title, cmd):
    """Run command string as subprocess"""
    try:
        cmd_list = shlex.split(cmd)
        output = subprocess.run(cmd_list, check=True)

        print(output)
    except subprocess.CalledProcessError as e:
        print("Error running command ", str(cmd))
        print(e.output)
        pass

    return


def worker():
    """receives messages from a pull subscription"""

    # create subscriber
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        "annaco-python-lib-test", "annaco-eod"
    )
    flow_control = pubsub_v1.types.FlowControl(
        max_messages=1,
        min_duration_per_lease_extension=600,
        max_duration_per_lease_extension=600,
        max_lease_duration=7200,
    )

    def callback(message):
        print(
            "Received message {} of message ID {}".format(message, message.message_id)
        )
        # Use `ack_with_response()` instead of `ack()` to get a future that tracks
        # the result of the acknowledge call. When exactly-once delivery is enabled
        # on the subscription, the message is guaranteed to not be delivered again
        # if the ack future succeeds.
        ack_future = message.ack_with_response()
        # ack message
        try:
            # Block on result of acknowledge call.
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            ack_future.result(timeout=200)
            print(f"Ack for message {message.message_id} successful.")
        except sub_exceptions.AcknowledgeError as e:
            print(
                f"Ack for message {message.message_id} failed with error: {e.error_code}"
            )
        print("Acknowledged message of message ID {}\n".format(message.message_id))

    future = subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control
    )
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            future.result()
        except:
            print("Exiting subscriber")
            future.cancel()


if __name__ == "__main__":
    worker()
