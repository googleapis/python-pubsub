# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-pubsub` client is a significant upgrade based
on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python),
and includes substantial interface changes. Existing code written for earlier versions
of this library will likely require updates to use this version. This document
describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an
[issue](https://github.com/googleapis/python-pubsub/issues).


## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Almost all methods that send requests to the backend expect request objects. We
provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-pubsub
```

* The script `fixup_pubsub_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.
Optionally, the `--use-keywords` switch can be added to generate flattened keyword
parameters instead of a request dictionary (see the following section for an
explanation).

```sh
$ scripts/fixup_pubsub_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import pubsub

publisher = pubsub.PublisherClient()

project_path = "projects/{}".format(PROJECT_ID)
topics = publisher.list_topics(project_path)
```


**After:**
```py
from google.cloud import pubsub

publisher = pubsub.PublisherClient()

project_path = f"projects/{PROJECT_ID}"
topics = publisher.list_topics(request={"project": project_path})
```

### More Details

In `google-cloud-pubsub<2.0.0`, parameters required by the API were positional
parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_topics(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, almost all methods that interact with the backend have a single
positional parameter `request`. Method docstrings indicate whether a parameter is
required or optional.

> **NOTE:** The exception are hand written methods such as `publisher.publish()` and
> `subscriber.subscribe()` that implement additional logic (e.g. request batching) and
> sit on top of the API methods from the generated parts of the library. The signatures
> of these methods have in large part been preserved.

Some methods have additional keyword only parameters. The available parameters depend
on the [`google.api.method_signature` annotation](https://github.com/googleapis/python-pubsub/blob/master/google/cloud/pubsub_v1/proto/pubsub.proto#L88)
specified by the API producer.


**After:**
```py
    def list_topics(
        self,
        request: pubsub.ListTopicsRequest = None,
        *,
        project: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTopicsPager:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are
> mutually exclusive. Passing both will result in an error.


Both of these calls are valid:

```py
response = client.list_topics(
    request={
        "project": project_path,
        "metadata": [("foo", "bar"), ("baz", "quux")],
    }
)
```

```py
response = client.list_topics(
    project=project_path,
    metadata=[("foo", "bar"), ("baz", "quux")],
)
```

This call is invalid because it mixes `request` with a keyword argument `metadata`.
Executing this code will result in an error:

```py
response = client.synthesize_speech(
    request={"project": project_path},
    metadata=[("foo", "bar"), ("baz", "quux")],
)
```

> **NOTE:** The `request` parameter of some methods can also contain a more rich set of
> options that are otherwise not available as explicit keyword only parameters, thus
> these _must_ be passed through `request`.


## Removed Utility Methods

> **WARNING**: Breaking change

Some utility methods such as publisher client's `subscription_path()` have been removed
and now only exist in the relevant client, e.g. `subscriber.subscription_path()`.

The `project_path()` method has been removed from both the publisher and subscriber
client, this path must now be constructed manually:
```py
project_path = f"project/{PROJECT_ID}"
```

## Removed `client_config` Parameter

The publisher and subscriber clients cannot be constructed with `client_config`
argument anymore. If you want to customize retry and timeout settings for a particular
method, you need to do it upon method invocation by passing the custom `timeout` and
`retry` arguments, respectively.
