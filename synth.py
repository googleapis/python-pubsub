# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import re
import textwrap

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
version = "v1"

# ----------------------------------------------------------------------------
# Generate pubsub GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="pubsub",
    version=version,
    bazel_target="//google/pubsub/v1:pubsub-v1-py",
    include_protos=True,
)
s.move(
    library,
    excludes=[
        "docs/**/*",
        "nox.py",
        "README.rst",
        "setup.py",
        "google/cloud/pubsub_v1/__init__.py",
        "google/cloud/pubsub_v1/types.py",
    ],
)

# DEFAULT SCOPES and SERVICE_ADDRESS are being used. so let's force them in.
s.replace(
    "google/pubsub_v1/services/*er/*client.py",
    r"DEFAULT_ENDPOINT = 'pubsub\.googleapis\.com'",
    """
    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub',
    )

    SERVICE_ADDRESS = "pubsub.googleapis.com:443"
    \"""The default address of the service.\"""

    \g<0>""",
)

# Monkey patch the streaming_pull() GAPIC method to disable pre-fetching stream
# results.
s.replace(
    "google/pubsub_v1/services/subscriber/client.py",
    r"(\s+#.+\n){2}\s+rpc = gapic_v1\.method\.wrap_method\(\s+self\._transport\.streaming_pull,",
    """
        # Wrappers in api-core should not automatically pre-fetch the first
        # stream result, as this breaks the stream when re-opening it.
        # https://github.com/googleapis/python-pubsub/issues/93#issuecomment-630762257
        self._transport.streaming_pull._prefetch_first_result_ = False

    \g<0>""",
)


# In Rertry config predicates, the last exception item lacks indentation.
s.replace(
    "google/pubsub_v1/services/publisher/client.py",
    r"^exceptions\.\w+,\n",
    " " * 20 + "\g<0>",
)

# Extract default publish() retry to a class variable for easier customization.
#
# The idea is to match several sections of the file that together form all of
# its contents. One of the subsections is the match that represents the default
# Retry object in the publish() method, and when concatenating the main file
# sections back together, the matched Retry definition is injected between them
# at the right place.
s.replace(
    "google/pubsub_v1/services/publisher/client.py",
    r"""
    (?P<part_1>.+?)
    (?P<part_2>^\s+SERVICE_ADDRESS\ =)
    (?P<part_3>.+?)
    (?P<matches_in_publish>
        (?P<before_match>
            \s+ self\._transport\.publish,\n
            \s+ default_retry=)
        (?P<default_retry>retries\.Retry\(
                             .+?
                             \),
                    .+?  \)),
    )
    (?P<part_5>.+?)
    """,
    (
        "\g<part_1>\n"
        "    # Copied from the publish() method with synth, do not inject it\n"
        "    # into the class by e.g. hardcoding it somewhere.\n"
        "    _DEFAULT_PUBLISH_RETRY = \g<default_retry>\n"
        "\g<part_2>\g<part_3>\g<matches_in_publish>\g<part_5>"
    ),
    re.VERBOSE | re.MULTILINE | re.DOTALL,
)

# Docstrings of *_iam_policy() methods are formatted poorly and must be fixed
# in order to avoid docstring format warnings in docs.
s.replace(
    "google/pubsub_v1/services/*er/client.py",
    r"(\s+)Args:",
    "\n\g<1>Args:"
)
s.replace(
    "google/pubsub_v1/services/*er/client.py",
    r"(\s+)\*\*JSON Example\*\*\s+::",
    "\n\g<1>**JSON Example**::\n",
)
s.replace(
    "google/pubsub_v1/services/*er/client.py",
    r"(\s+)\*\*YAML Example\*\*\s+::",
    "\n\g<1>**YAML Example**::\n",
)
s.replace(
    "google/pubsub_v1/services/*er/client.py",
    r"(\s+)For a description of IAM and its features, see",
    "\n\g<0>",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    samples=True,
    cov_level=99,
    system_test_external_dependencies=["psutil"],
)
s.move(templated_files, excludes=[".coveragerc"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
