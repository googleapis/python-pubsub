# Copyright 2017, Google LLC All rights reserved.
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

from opentelemetry.propagators.textmap import Setter

from google.pubsub_v1 import types as gapic_types


class OpenTelemetryContextSetter(Setter):
    """
    Used by Open Telemetry for context propagation.
    """

    def set(self, carrier: gapic_types.PubsubMessage, key: str, value: str) -> None:
        """
        Injects trace context into Pub/Sub message attributes with
        "googclient_" prefix.
        """
        carrier.attributes["googclient_" + key] = value