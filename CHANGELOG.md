# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-pubsub/#history


## [2.2.0](https://www.github.com/googleapis/python-pubsub/compare/v2.1.0...v2.2.0) (2020-11-16)


### Features

* Add dead lettering max delivery attempts argument ([#236](https://www.github.com/googleapis/python-pubsub/issues/236)) ([7687ae5](https://www.github.com/googleapis/python-pubsub/commit/7687ae500bdb9c76e3ffb23302b4f32dc9627d81))
* Enable server side flow control by default with the option to turn it off ([#231](https://www.github.com/googleapis/python-pubsub/issues/231)) ([94d738c](https://www.github.com/googleapis/python-pubsub/commit/94d738c07c6404a152c6729f5ba4b106b1fe9355))


### Bug Fixes

* fix mtls issue in handwritten layer ([#226](https://www.github.com/googleapis/python-pubsub/issues/226)) ([09a409c](https://www.github.com/googleapis/python-pubsub/commit/09a409c6240a74dcb46d8f3f86d4fb95a52274a7))
* make fixup script consistent with migration docs ([#208](https://www.github.com/googleapis/python-pubsub/issues/208)) ([b64e218](https://www.github.com/googleapis/python-pubsub/commit/b64e2187ab0810437575580d6ddb5315ff60e274))


### Documentation

* document potentially unexpected blocking behavior of publish() method ([#214](https://www.github.com/googleapis/python-pubsub/issues/214)) ([b6d9bd7](https://www.github.com/googleapis/python-pubsub/commit/b6d9bd7c38d4fe597c25b7b5869fd4a1259c7687))
* fix get topic_path in subscriber sample ([#210](https://www.github.com/googleapis/python-pubsub/issues/210)) ([7228f6c](https://www.github.com/googleapis/python-pubsub/commit/7228f6c9a4c050bf22bb4bc3582b89b04eaa8702))

## 2.1.0

09-21-2020 02:19 PDT


### Implementation Changes

- Convert all RPC error types to exceptions. ([#163](https://github.com/googleapis/python-pubsub/issues/163)) ([#170](https://github.com/googleapis/python-pubsub/pull/170))
- Pass client options to publisher and subscriber clients. ([#166](https://github.com/googleapis/python-pubsub/issues/166)) ([#190](https://github.com/googleapis/python-pubsub/pull/190))


### New Features

- Regenerate the client lib to pick new mtls env (via synth). ([#197](https://github.com/googleapis/python-pubsub/pull/197))


### Documentation

- Add subscription detachment sample. ([#152](https://github.com/googleapis/python-pubsub/pull/152))
- Use new call syntax in subscriber docs. ([#198](https://github.com/googleapis/python-pubsub/issues/198)) ([#203](https://github.com/googleapis/python-pubsub/pull/203))


### Internal / Testing Changes

- Update CODEOWNERS. ([#193](https://github.com/googleapis/python-pubsub/pull/193))

## 2.0.0

09-11-2020 05:03 PDT


### Implementation Changes

- Transition the library to microgenerator. ([#158](https://github.com/googleapis/python-pubsub/pull/158))
  This is a **breaking change** that introduces several **method signature changes** and **drops support
  for Python 2.7 and 3.5**.

### Documentation

- Add samples for using ordering keys. ([#156](https://github.com/googleapis/python-pubsub/pull/156))
- Remove extra white space in delivery attempt sample. ([#159](https://github.com/googleapis/python-pubsub/pull/159))

### Internal / Testing Changes

- Fix flaky sequencer unit tests. ([#187](https://github.com/googleapis/python-pubsub/pull/187))

## [1.7.0](https://www.github.com/googleapis/python-pubsub/compare/v1.6.1...v1.7.0) (2020-07-13)

This is the last release that supports Python 2.7 and 3.5.

### New Features

- Add support for server-side flow control. ([#143](https://github.com/googleapis/python-pubsub/pull/143)) ([04e261c](https://www.github.com/googleapis/python-pubsub/commit/04e261c602a2919cc75b3efa3dab099fb2cf704c))

### Dependencies

- Update samples dependency `google-cloud-pubsub` to `v1.6.1`. ([#144](https://github.com/googleapis/python-pubsub/pull/144)) ([1cb6746](https://github.com/googleapis/python-pubsub/commit/1cb6746b00ebb23dbf1663bae301b32c3fc65a88))

### Documentation

- Add pubsub/cloud-client samples from the common samples repo (with commit history). ([#151](https://github.com/googleapis/python-pubsub/pull/151)) 
- Add flow control section to publish overview. ([#129](https://github.com/googleapis/python-pubsub/pull/129)) ([acc19eb](https://www.github.com/googleapis/python-pubsub/commit/acc19eb048eef067d9818ef3e310b165d9c6307e))
- Add a link to Pub/Sub filtering language public documentation to `pubsub.proto`. ([#121](https://github.com/googleapis/python-pubsub/pull/121)) ([8802d81](https://www.github.com/googleapis/python-pubsub/commit/8802d8126247f22e26057e68a42f5b5a82dcbf0d))


## [1.6.1](https://www.github.com/googleapis/python-pubsub/compare/v1.6.0...v1.6.1) (2020-06-30)


### Documentation

* added Python2 sunset notice (synth) ([#140](https://www.github.com/googleapis/python-pubsub/issues/140)) ([c8f6378](https://www.github.com/googleapis/python-pubsub/commit/c8f63788636c2e3436c8ce6a01ef3b59e3df772a))
* explain how to nack a sync pull message ([#123](https://www.github.com/googleapis/python-pubsub/issues/123)) ([f2eec65](https://www.github.com/googleapis/python-pubsub/commit/f2eec65cec43066ba7a2d1d45efa979e6b7add4f))

## [1.6.0](https://www.github.com/googleapis/python-pubsub/compare/v1.5.0...v1.6.0) (2020-06-09)


### Features

* Add flow control for message publishing ([#96](https://www.github.com/googleapis/python-pubsub/issues/96)) ([06085c4](https://www.github.com/googleapis/python-pubsub/commit/06085c4083b9dccdd50383257799904510bbf3a0))


### Bug Fixes

* Fix PubSub incompatibility with api-core 1.17.0+ ([#103](https://www.github.com/googleapis/python-pubsub/issues/103)) ([c02060f](https://www.github.com/googleapis/python-pubsub/commit/c02060fbbe6e2ca4664bee08d2de10665d41dc0b))


### Documentation
- Clarify that Schedulers shouldn't be used with multiple SubscriberClients ([#100](https://github.com/googleapis/python-pubsub/pull/100)) ([cf9e87c](https://github.com/googleapis/python-pubsub/commit/cf9e87c80c0771f3fa6ef784a8d76cb760ad37ef))
- Fix update subscription/snapshot/topic samples ([#113](https://github.com/googleapis/python-pubsub/pull/113)) ([e62c38b](https://github.com/googleapis/python-pubsub/commit/e62c38bb33de2434e32f866979de769382dea34a))


### Internal / Testing Changes
- Re-generated service implementaton using synth: removed experimental notes from the RetryPolicy and filtering features in anticipation of GA, added DetachSubscription (experimental) ([#114](https://github.com/googleapis/python-pubsub/pull/114)) ([0132a46](https://github.com/googleapis/python-pubsub/commit/0132a4680e0727ce45d5e27d98ffc9f3541a0962))
- Incorporate will_accept() checks into publish() ([#108](https://github.com/googleapis/python-pubsub/pull/108)) ([6c7677e](https://github.com/googleapis/python-pubsub/commit/6c7677ecb259672bbb9b6f7646919e602c698570))

## [1.5.0](https://www.github.com/googleapis/python-pubsub/compare/v1.4.3...v1.5.0) (2020-05-04)


### Features

* add methods for listing snapshots (via synth) ([#66](https://www.github.com/googleapis/python-pubsub/issues/66)) ([4ce898e](https://www.github.com/googleapis/python-pubsub/commit/4ce898e80eeb16b18d1ee29c678ade149804d186))
* send client id with StreamingPullRequest ([#58](https://www.github.com/googleapis/python-pubsub/issues/58)) ([9f8acfa](https://www.github.com/googleapis/python-pubsub/commit/9f8acfacfbe93224f59439bb51a17fc28b06c22a)), closes [#62](https://www.github.com/googleapis/python-pubsub/issues/62)

## [1.4.3](https://www.github.com/googleapis/python-pubsub/compare/v1.4.2...v1.4.3) (2020-04-16)


### Bug Fixes

* fix docs warnings in Sphinx 3.0+ ([#70](https://www.github.com/googleapis/python-pubsub/issues/70)) ([21e761e](https://www.github.com/googleapis/python-pubsub/commit/21e761ee89a4c03e105dc9cddbab0a34be9a9fda))
* restrict api-core dependency to < 1.17.0 ([#76](https://www.github.com/googleapis/python-pubsub/issues/76)) ([191b051](https://www.github.com/googleapis/python-pubsub/commit/191b0516335f5c60828a818ba79e99d6c68aa7bd))

## [1.4.2](https://www.github.com/googleapis/python-pubsub/compare/v1.4.1...v1.4.2) (2020-03-25)

### Bug Fixes

* update generated retry timings for publish and pull rpcs via synth ([#43](https://www.github.com/googleapis/python-pubsub/issues/43)) ([4f7fe85](https://www.github.com/googleapis/python-pubsub/commit/4f7fe85618d811fea94cb46b5dc758aa78c328a8))
* use client_options.api_endpoint parameter instead of ignoring it ([#59](https://www.github.com/googleapis/python-pubsub/issues/59)) ([56b8d7b](https://www.github.com/googleapis/python-pubsub/commit/56b8d7b046a495ce2ce59bebdd354385147a5013)), closes [#61](https://www.github.com/googleapis/python-pubsub/issues/61)

## [1.4.1](https://www.github.com/googleapis/python-pubsub/compare/v1.4.0...v1.4.1) (2020-03-23)

### Bug Fixes

* Don't assert on unordered publishes after publish error. ([#49](https://www.github.com/googleapis/python-pubsub/issues/49)) ([ea19ce6](https://www.github.com/googleapis/python-pubsub/commit/ea19ce616f6961e8993b72cd2921f7f3e61541f9))

## [1.4.0](https://www.github.com/googleapis/python-pubsub/compare/v1.3.1...v1.4.0) (2020-03-06)

### Features

* **pubsub:** implement max_duration_per_lease_extension option ([#38](https://www.github.com/googleapis/python-pubsub/issues/38)) ([d911a2d](https://www.github.com/googleapis/python-pubsub/commit/d911a2dc8edf3c348ad3f128368b30e32dbc449e))

## [1.3.1](https://www.github.com/googleapis/python-pubsub/compare/v1.3.0...v1.3.1) (2020-02-28)

### Bug Fixes

* shutdown error on streaming pull callback error ([#40](https://www.github.com/googleapis/python-pubsub/issues/40)) ([552539e](https://www.github.com/googleapis/python-pubsub/commit/552539e7beb30833c39dd29bfcb0183a07895f97))

## [1.3.0](https://www.github.com/googleapis/python-pubsub/compare/v1.2.0...v1.3.0) (2020-02-20)

### Features

* **pubsub:** ordering keys ([#26](https://www.github.com/googleapis/python-pubsub/issues/26)) ([cc3093a](https://www.github.com/googleapis/python-pubsub/commit/cc3093a2c0304259bc374bc2eeec9630e4a11a5e))
* add context manager capability to subscriber ([#32](https://www.github.com/googleapis/python-pubsub/issues/32)) ([b58d0d8](https://www.github.com/googleapis/python-pubsub/commit/b58d0d8e404c0a085b89d3407e6640651e81568c))

## [1.2.0](https://www.github.com/googleapis/python-pubsub/compare/v1.1.0...v1.2.0) (2020-02-05)

### Features

* **pubsub:** add delivery attempt property to message object received by user code ([#10205](https://www.github.com/googleapis/google-cloud-python/issues/10205)) ([a0937c1](https://www.github.com/googleapis/python-pubsub/commit/a0937c13107b92271913de579b60f24b2aaac177))
* add `StreamingPullRequest.client_id` field (via synth) ([199d56a](https://www.github.com/googleapis/python-pubsub/commit/199d56a939bb6244f67138f843dafdd80721f0d3))

### Bug Fixes

* **pubsub:** handle None in on response callback ([#9982](https://www.github.com/googleapis/google-cloud-python/issues/9982)) ([6596c4b](https://www.github.com/googleapis/python-pubsub/commit/6596c4bae5526d82f5c1b5e0c243b2883404d51f))
* replace unsafe six.PY3 with PY2 for better future compatibility with Python 4 ([#10081](https://www.github.com/googleapis/google-cloud-python/issues/10081)) ([975c1ac](https://www.github.com/googleapis/python-pubsub/commit/975c1ac2cfdac0ce4403c0b56ad19f2ee7241f1a))

## 1.1.0

12-09-2019 18:51 PST

### Implementation Changes
- Update client configurations (via synth). ([#9784](https://github.com/googleapis/google-cloud-python/pull/9784))
- Include request overhead when computing publish batch size overflow. ([#9911](https://github.com/googleapis/google-cloud-python/pull/9911))
- Split large (mod)ACK requests into smaller ones. ([#9594](https://github.com/googleapis/google-cloud-python/pull/9594))
- Fix messages delivered multiple times despite a long ACK deadline. ([#9525](https://github.com/googleapis/google-cloud-python/pull/9525))
- Update batching and flow control parameters to be same as the other client libraries. ([#9597](https://github.com/googleapis/google-cloud-python/pull/9597))
- Add `StreamingPullManager._should_terminate`. ([#9335](https://github.com/googleapis/google-cloud-python/pull/9335))

### New Features
- Add stop method. ([#9365](https://github.com/googleapis/google-cloud-python/pull/9365))

### Dependencies
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

### Documentation
- Change spacing in docs templates (via synth). ([#9759](https://github.com/googleapis/google-cloud-python/pull/9759))

### Internal / Testing Changes
- Refactor fake leaser test helper. ([#9632](https://github.com/googleapis/google-cloud-python/pull/9632))
- Add subscriber role test for streaming. ([#9507](https://github.com/googleapis/google-cloud-python/pull/9507))

## 1.0.2

09-30-2019 11:57 PDT


### Implementation Changes

- Streaming pull shouldn't need `subscriptions.get` permission ([#9360](https://github.com/googleapis/google-cloud-python/pull/9360)).

## 1.0.1

09-27-2019 07:01 PDT


### Implementation Changes
- Set default stream ACK deadline to subscriptions'. ([#9268](https://github.com/googleapis/google-cloud-python/pull/9268))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Link to correct TimeoutError in futures docs. ([#9216](https://github.com/googleapis/google-cloud-python/pull/9216))

### Internal / Testing Changes
- Adjust messaging RPC timeout settings (via synth). [#9279](https://github.com/googleapis/google-cloud-python/pull/9279)

## 1.0.0

08-29-2019 09:27 PDT

### Implementation Changes
- Add 'ReceivedMessage.delivery_attempt' field (via synth). ([#9098](https://github.com/googleapis/google-cloud-python/pull/9098))
- Remove send/recv msg size limit, update docstrings (via synth). ([#8964](https://github.com/googleapis/google-cloud-python/pull/8964))

### Documentation
- Update docstrings for client kwargs and fix return types uris ([#9037](https://github.com/googleapis/google-cloud-python/pull/9037))
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Add dead-letter-policy field in preparation for its implementation (via synth) ([#9078](https://github.com/googleapis/google-cloud-python/pull/9078))

## 0.45.0

07-31-2019 02:03 PDT


### Implementation Changes

- Remove deprecated methods and settings ([#8836](https://github.com/googleapis/google-cloud-python/pull/8836))


### Documentation

- Use double backticks for ReST correctness. ([#8829](https://github.com/googleapis/google-cloud-python/pull/8829))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.44.0

07-29-2019 04:28 PDT


### Implementation Changes

- PubSub: Deprecate several FlowControl settings and things in Message class ([#8796](https://github.com/googleapis/google-cloud-python/pull/8796))

### Documentation

- Pub/Sub: document regional endpoint ([#8789](https://github.com/googleapis/google-cloud-python/pull/8789))

## 0.43.0

07-24-2019 17:13 PDT


### Implementation Changes
- Accomodate new location of 'IAMPolicyStub' (via synth). ([#8680](https://github.com/googleapis/google-cloud-python/pull/8680))
- Use kwargs in test_subscriber_client ([#8414](https://github.com/googleapis/google-cloud-python/pull/8414))

### New Features
- Add `options_` argument to clients' `get_iam_policy`; pin black version (via synth). ([#8657](https://github.com/googleapis/google-cloud-python/pull/8657))
- Add 'client_options' support, update list method docstrings (via synth). ([#8518](https://github.com/googleapis/google-cloud-python/pull/8518))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix typo in publisher index. ([#8619](https://github.com/googleapis/google-cloud-python/pull/8619))
- Document how to choose the PubSub auth method ([#8429](https://github.com/googleapis/google-cloud-python/pull/8429))
- Document different PuSub received message types ([#8468](https://github.com/googleapis/google-cloud-python/pull/8468))
- PubSub: Document batch settings, make synth operations idempotent ([#8448](https://github.com/googleapis/google-cloud-python/pull/8448))
- Add custom docstrings for FlowControl enum and values (via synth). ([#8426](https://github.com/googleapis/google-cloud-python/pull/8426))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Add system tests for PubSub clients ([#8277](https://github.com/googleapis/google-cloud-python/pull/8277))

## 0.42.1

06-18-2019 15:14 PDT


### Implementation Changes
- Increase the minimum allowed version for api core. ([#8419](https://github.com/googleapis/google-cloud-python/pull/8419))
- Allow kwargs to be passed to create_channel. ([#8399](https://github.com/googleapis/google-cloud-python/pull/8399))

## 0.42.0

06-18-2019 11:32 PDT

### Implementation Changes
- Core: Mitigate busy reopen loop in ResumableBidiRpc consuming 100% CPU ([#8193](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8193))
- Pub/Sub: Increase initial_rpc_timeout for messaging (via synth). ([#8219](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8219))
- PubSub: Release the state lock before calling the publish api ([#8234](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8234))
- Pub/Sub: Expose publish retry settings ([#8231](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8231))
- Prevent unhandled background error on SPM shutdown ([#8111](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8111))
- Update timeouts, blacken noxfile.py, setup.py (via synth). ([#8128](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8128))
- PubSub: Fix streaming pull incorrectly handling FlowControl max_messages setting ([#7948](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7948))

### Documentation
- Document PubSub FlowControl settings ([#8293](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8293))
- Replace readthedocs links with links to github docs. ([#8291](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8291))
- Pub/Sub: surface publish future in documentation ([#8229](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8229))
- Pubsub: Separate subscriber and publish future documentation. ([#8205](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8205))
- Drop mention of long-removed 'policy' object. ([#8081](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8081))

### Internal / Testing Changes
- Pub/Sub: staticmethod check ([#8091](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8091))
- Add empty lines (via synth). ([#8067](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8067))

## 0.41.0

05-15-2019 13:57 PDT


### New Features
- Add `kms_key_name` arg to `create_topic`; remove BETA warnings (via synth). ([#7936](https://github.com/googleapis/google-cloud-python/pull/7936))
- Add message ordering (via synth). ([#7551](https://github.com/googleapis/google-cloud-python/pull/7551))

### Implementation Changes
- Propagate subscribe callback errors to main thread ([#7954](https://github.com/googleapis/google-cloud-python/pull/7954))
- Fix pubsub Streaming Pull shutdown on RetryError ([#7863](https://github.com/googleapis/google-cloud-python/pull/7863))
- Make PubSub subscriber Scheduler inherit from ABC ([#7690](https://github.com/googleapis/google-cloud-python/pull/7690))
- Add routing header to method metadata (via synth). ([#7623](https://github.com/googleapis/google-cloud-python/pull/7623))

### Internal / Testing Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Add nox session `docs` (via synth). ([#7778](https://github.com/googleapis/google-cloud-python/pull/7778))
- Pub/Sub (nit): wrong var name in sample ([#7705](https://github.com/googleapis/google-cloud-python/pull/7705))

## 0.40.0

03-15-2019 14:09 PDT


### Implementation Changes
- Propagate 'RetryError' in 'PublisherClient.publish'. ([#7071](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7071))
- Protoc-generated serialization update.. ([#7091](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7091))

### New Features
- Add 'authentication_method' to 'PushConfig' (via synth). ([#7512](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7512))
- Add protos as an artifact to library ([#7205](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7205))
- Pub/sub: pass transport w/ custom channel to GAPIC API clients. ([#7008](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7008))

### Dependencies

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7307))
- Update copyright headers
- Fix broken docstring cross-reference links. ([#7132](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7132))
- Docstring changes from updates to .proto files. ([#7054](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7054))
- Pick up stub docstring fix in GAPIC generator. ([#6978](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6978))

### Internal / Testing Changes
- Copy proto files alongside protoc versions.

## 0.39.1

12-17-2018 16:57 PST


### Implementation Changes
- Initialize `StreamingPullFuture._cancelled` as True. ([#6901](https://github.com/googleapis/google-cloud-python/pull/6901))
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Emphasize that returned futures may differ from stdlib futures. ([#6875](https://github.com/googleapis/google-cloud-python/pull/6875))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 0.39.0

11-27-2018 13:32 PST

### Implementation Changes
- Pick up fixes to GAPIC generator. ([#6503](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6503))
- Override client classmethod factories inherited from GAPIC. ([#6453](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6453))
- Fix imports for hand-written client docstring examples. ([#6345](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6345))
- Fix path for patch of 'bidi' elements. ([#6243](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6243))
- Move bidi to api-core. ([#6211](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6211))
- Re-generate library using pubsub/synth.py ([#6059](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6059))
- Re-generate library using pubsub/synth.py ([#5978](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5978))

### New Features
- Add 'expiration_policy' to subscriber client. ([#6223](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6223))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6391))
- Update IAM version in dependencies. ([#6362](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6362))
- Bump minimum 'api_core' version to '1.4.1'. ([#6134](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6134))

### Documentation
- Fix client_info bug, update docstrings. ([#6418](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6418))
- Fix docstring reference to wrong future class. ([#6382](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6382))
- Normalize use of support level badges. ([#6159](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6159))
- Update subscriber example in README to current patterns. ([#6194](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6194))
- Prep pubsub docs for repo split. ([#6001](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6001))

### Internal / Testing Changes
- Fix error from new flake8 version. ([#6346](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6346))
- Use new Nox. ([#6175](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6175))

## 0.38.0

### Implementation Changes

- Fix race condition in recv()'s usage of self.call. ([#5935](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5935))
- Re-generate the underlying library from protos. ([#5953](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5953))
- Change 'BatchSettings.max_bytes' default. ([#5899](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5899))
- Fix race condition where pending Ack IDs can be modified by another thread. ([#5929](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5929))

### Internal / Testing Changes

- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))

## 0.37.2

### Implementation Changes

- Fix classmethod wrapping (#5826)

### Documentation

- Fix Sphinx rendering for publisher client. (#5822)

### Internal / Testing Changes

- Re-generate library, removing obsolete synth modifications. (#5825)
- Add test for testing invoking a wrapped class method on the class itself (#5828)

## 0.37.1

### Implementation Changes

- Make get_initial_request more resilient to race conditions. (#5803)

## 0.37.0

### Implementation Changes

- Make Publisher batch-related interfaces private (#5784)

## 0.36.0

### Implementation Changes
- Pubsub: Make 'Message.publish_time' return datetime (#5633)
- Ensure SPM methods check that 'self._consumer' is not None before use. (#5758)

### New Features
- PubSub: add geo-fencing support (#5769)
- Add 'Message.ack_id' property. (#5693)

## 0.35.4

### Implementation Changes

- Recover streams during the gRPC error callback. (#5446)
- Use operational lock when checking for activity on streams. (#5445)

## 0.35.3

### Implementation Changes

- Add additional error handling to unary RPCs (#5438)

## 0.35.2

### Implementation Changes
- Add heartbeating to the streaming pull manager (#5413)
- Fix retrying of bidirectional RPCs and closing the streaming pull manager (#5412)

## 0.35.1

### Implementation Changes
- Catch errors when re-retying send() or recv() in addition to open() (#5402)

## 0.35.0

### Implementation Changes

- Send requests during streaming pull over a separate unary RPC (#5377)
- Initialize references to helper threads before starting them (#5374)
- Make leaser exit more quickly (#5373)
- Make re-open failures bubble to callbacks (#5372)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Normalize overflow handling for max count and bytes (#5343)

### New Features

- Restore the synchronous pull method (#5379)
- Promote subscribe_experimental() to subscribe(), remove old subscriber implementation. (#5274)
- Wire up scheduler argument for subscribe() (#5279)

### Documentation

- Add link to streaming pull behavior documentation (#5378)
- Fix example in subscribe's documentation (#5375)

### Internal / Testing Changes

- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.34.0

### Implementation Changes

- Lower the flow control defaults. (#5248)

### New Features

- A new implementation of the subscriber has been added. This is available as `SubscriberClient.subscribe_experimental`. In the next release, this will be replace the current `subscribe` method. If you use this, please report your findings to us on GitHub. (#5189, #5201, #5210, #5229, #5230, #5237, #5256)

### Dependencies

- Remove psutil dependency. (#5248)

## 0.33.1

### Implementation changes

- Surface publish RPC errors back to the publish futures (#5124)
- Make the pausable response iterator aware of the RPC state to prevent deadlock (#5108)
- Properly handle graceful stop in request generator (#5097)

## 0.33.0

### Implementation changes

- Drop leased messages after flow_control.max_lease_duration has passed. (#5020)
- Fix mantain leases to not modack messages it just dropped (#5045)
- Avoid race condition in maintain_leases by copying leased_messages (#5035)
- Retry subscription stream on InternalServerError, Unknown, and GatewayTimeout (#5021)
- Use the rpc's status to determine when to exit the request generator thread (#5054)
- Fix missing iter on request stream (#5078)
- Nack messages when the subscriber callback errors (#5019)

### Testing

- pubsub nox.py cleanup (#5056)
- Fix test that checks for retryable exceptions (#5034)

## 0.32.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)

## 0.32.0

### Implementation changes

- Added support for streaming pull receipts. (#4878)

## 0.31.0

### New features

- Added the ability for subscriber to batch requests. (#4895)
- Added pending request backpressure for subscriber. (#4892)

### Implementation changes

- Raise `ValueError` when a message is too large for a batch. (#4872)
- Updated the default batch size to 10 MB. (#4857)
- Allow a custom `Event` type in Pub / Sub futures. (#4643)

### Documentation

- Clarify that `modify_ack_deadline` resets the deadline. (#4822)

### Testing

- Fix unit test for default `max_bytes` value. (#4860)

## 0.30.1

### Notable Implementation Changes

- Moving lock factory used in publisher client to the Batch
  implementation (#4628).
- Use a UUID (rather than a sentinel object) on `Future` (#4634).
- Apply scopes to explicitly provided credentials if needed (#4594).
  Fixes #4479. This feature comes as part of `google-api-core==0.1.3`.

### Dependencies

- Upgrading to `google-api-core==0.1.3` which depends on the latest
  `grpcio==1.8.2` (#4642). This fixes #4600. For details, see related
  gRPC [bug](https://github.com/grpc/grpc/issues/9688) and
  [fix](https://github.com/grpc/grpc/pull/13665).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.30.1/

## 0.30.0

### Notable Implementation Changes

- Dropping redundant `Policy._paused` data member (#4568).
- Removing redundant "active" check in policy (#4603).
- Adding a `Consumer.active` property (#4604).
- Making it impossible to call `Policy.open()` on an already opened
  policy (#4606).
- **Bug fix** (#4575): Fix bug with async publish for batches. There
  were two related bugs. The first: if a batch exceeds the `max_messages`
  from the batch settings, then the `commit()` will fail. The second:
  when a "monitor" worker calls `commit()` after `max_latency` seconds,
  a failure can occur if a new message is added to the batch **during**
  the commit. To fix, the following changes were implemented:

  - Adding a "STARTING" status for `Batch.commit()` (#4614). This
    fixes the issue when the batch exceeds `max_messages`.
  - Adding extra check in `Batch.will_accept` for the number of
    messages (#4612).
  - Moving `will_accept()` check out of `PublisherClient.batch()`
    factory (#4613).
  - Checking `Batch.will_accept` in thread-safe way (#4616).
- **Breaking API change**: As part of #4613, changing `PublisherClient.batch()`
  to no longer accept a `message` (since the `will_accept` check needs to
  happen in a more concurrency friendly way). In addition, changing the
  `create` argument so that it means "create even if batch already exists"
  rather than "create if missing".

### Documentation

- Add more explicit documentation for `Message.attributes` (#4601).
- Make `Message.__repr__` a bit prettier / more useful (#4602).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.30.0/

## 0.29.4

### Notable Implementation Changes

- **Bug fix**: Restore previous behavior of the subscription lease
  maintenance worker. This was accidentally "stopped" in `0.29.3`
  due to a change in implementation that went from an `active`
  boolean to an "inactive" / `stopped` boolean, so `True` became
  `False` and vice-versa (#4564).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.4/

## 0.29.3

### Notable Implementation Changes

- In subscription consumer thread: Making sure the request generator
  attached to an inactive bidirectional streaming pull is stopped before
  spawning a new request generator. This way we have a (fairly strong)
  guarantee that requests in the queue don't get sent into an inactive
  stream (#4503, #4554).
- Adding `pause` / `resume` to subscription consumer thread and using these
  methods during flow control. The previous implementation tried to close the
  subscription (which involved 3 worker threads and 10 executors in a thread
  pool) and then re-open a new subscription. But, this was not entirely
  possible to shut down correctly from **within** one of the worker threads.
  Instead, we only pause the worker (of the 3) that is pulling new responses
  from the bidirectional streaming pull (#4558).
- **Bug fix** (#4516): Using `max` where `min` was used by mistake to
  ensure the number of bytes tracked for subscription flow control
  remained non-negative (#4514).
- Raising `TypeError` if `SubscriberClient.subscribe` receives a
  non-callable callback (#4497).
- Shutting down thread pool executor when closing a subscriber
  policy (#4522).
- Renaming `Policy.on_callback_request` to `Policy.dispatch_callback`
  and making the behavior much less dynamic (#4511).
- Make sure subscription consumer thread doesn't try to join itself
  when exiting in error (#4540).

### Dependencies

- Upgrading `google-api-core` dependency to latest revision (`0.1.2`)
  since we rely on the latest version of the `concurrent.futures` backport
  to provide the `thread_name_prefix` argument for thread pool
  executor (#4521, #4559).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.3/

## 0.29.2

### Notable Implementation Changes

- **Bug fix** (#4463): Making a subscription consumer actually stop
  running after encountering an exception (#4472, #4498). This bug
  is the **only** reason for the `0.29.2` release.
- Thread Changes

  - Added names to all threads created directly by Pub / Sub (#4474,
    #4476, #4480). Also removing spaces and colons from thread
    names (#4476).
- Logging changes

  - Adding debug logs when lease management exits (#4484)
  - Adding debug logs when `QueueCallbackThread` exits (#4494).
    Instances handle the processing of messages in a
    subscription (e.g. to `ack`).
  - Using a named logger in `publisher.batch.thread` (#4473)
  - Adding newlines before logging protobuf payloads (#4471)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.2/

## 0.29.1

### Notable Implementation Changes

- **Bug fix** (#4234): Adding retries for connection `UNAVAILABLE`. This
  bug made the Pub / Sub client mostly unusable for subscribers to topics
  that don't have a steady stream of messages. After ~2 minutes of inactivity,
  the gRPC connection would timeout and raise `UNAVAILABLE` locally, i.e. not
  due to a response from the backend. (#4444)
- Updating autogenerated packages (#4438)

### Documentation

- Fixing broken examples in quick start (#4398)
- Fixing broken example in README (#4402, h/t to @mehmetboraezer)
- Updating old/dead link to usage doc in README (#4406, h/t to @mehmetboraezer)

### Dependencies

- Dropping dependency on `google-cloud-core` in exchange for
  `google-api-core` (#4438)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.1/

## 0.29.0

### Notable Implementation Changes

- Honor `max_messages` always (#4262)
- Add futures for subscriptions (#4265)
- Set gRPC message options and keepalive (#4269)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos` dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.0/
