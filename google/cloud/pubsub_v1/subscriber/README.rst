===============
Subscriber APIs
===============

There are two subscriber APIs:

- `Single-batch single-threaded pull <https://googleapis.dev/python/pubsub/latest/subscriber/index.html#pulling-a-subscription-synchronously>`_

  A single batch of messages is retrieved and processed.

  Of course, this could be used in a loop to handle many messages over a long time.

- `Multi-threaded long-running <https://googleapis.dev/python/pubsub/latest/subscriber/index.html#pulling-a-subscription-asynchronously>`_

  Multiple threads are used to:

  - Process multiple messages in parallel using a thread pool.
  - Communicate with the server to handle leases and flow control with
    dedicated threads, separate from the threads processing messages.


Multi-threaded subscriber
========================

The multi-threaded subscriber consists of several components and
threads.

Components:

Manager
  `._protocol.streaming_pull_manager.StreamingPullManager`

  The manager sets up the various components.

  It also:
  - Receives messages to be processed from the consumer.
  - Pauses and resumes the consumer based on workload, to avoid
    accumulating too many unprocessed messages.

  The manager doesn't have/manage a thread of its own.  Most of it's
  work is done in response to messages from the consumer, dispatcher,
  leaser, and heartbeat threads.

Consumer
  `google.api_core.bidi.BackgroundConsumer`

  The consumer runs as a separate thread, receiving messages to be
  processed and sending them to the manager (via it's `_on_response`
  method).

Dispatcher
  `._protocol.dispatcher.Dispatcher`

  The dispatcher is the means by which workers communicate status with
  the rest of the system by sending message-status events:

  ack
    The message was processed and the server should consider it
    handled.

  nack
    Tell the server we've abandoned the message and that it should
    send it to another subscriber.

  modify_ack_deadline
    Tell the server how long to expect to wait for the message to be handled.

    This is triggered by the manager when it receives a message.

    .. We could avoid this if our deadline was <= server deadline.

    A message handler could trigger this as well.

    .. This seems unlikely, as this would be overridden the next time
       the leaser ran.

  drop
    Drop a message without notifying the server.

    .. It's unclear what the use case for this would be.

  The dispatcher runs a dedicated thread that listens on a queue.

  .. Weirdly, the queue it uses is from the Scheduler, which doesn't
     use it's own queue. :/

Leaser
  `._protocol.leaser.Leaser`

  When the manager receives a message, it considers it to be "leased".
  The lease has a deadline, which may be extended.  The lease extends
  until the message is acked/completed, nacked/abandoned or until the
  server expires it.  The leaser takes care of:

  - Extending leases while they're still being worked on, or
  - Nacking leases that have gone too long.

  The most important of these is lease extension, so that messages
  don't expire if processing them takes longer than expected.

  The leaser has a dedicated thread.

Scheduler
  `scheduler.ThreadScheduler`

  Manages a thread pool used for handling messages.

  .. It has a queue that's used by the dispatcher. That's silly. :)


Messages on hold
  `._protocol.messages_on_hold.MessagesOnHold`

  Buffers received messages.

  - The main purpose is to maintaining message ordering.  Messages can
    normally be processed in any order. If a group of messages has the
    same non-empty ordering key, then they will be executed in order.
    Only one of these messages can be executed at a time.  This may
    delay message execution, requiring that messages be held.

  - If our load is >= 1, then we need to buffer unordered messages
    too.

  The logic for releasing messages is spread between the manager and
  the messages on hold component in odd ways.

  Unordered messages are only released if the manager load is < 1, but
  ordered messages are released without regard to manager load.

  The load computation excludes on-hold messages.  We could accumulate
  an unbound number of ordered messages.  That seems like a bad idea.
  One of the reasons to pause the consumer is to avoid accumulating a
  lot of queued work.

  It seems that:

  - Load should count all unfinished messages, so we don't accumulate
    them in memory, because we pause the consumer.

  - We should just schedule unordered messages right away, regardless
    of load. One queue (the thread-pool queue) seems as good as
    another (the held messages).

  If we did this, then we could simplify this logic, possibly quite a bit.

Heartbeater
  `._protocol.heartbeater.Heartbeater`

  Calls the `heartbeat` method on the manager every 30 seconds, which
  then sends a heartbeat message to the server.

  It uses a dedicated thread.


Threads
-------

- Scheduler thread pool (multiple threads)
- Consumer
- Dispatcher
- Leaser
- Heartbeater.


Locking notes
-------------

Locks are a consequence of shared mutable state. Shared mutable state
is a bug magnet. :)

- The dispatcher has an `_operational_lock`.   It needs this because
  the manager can call it directly.  This could be avoided if the
  manager only communicated using the dispatcher's queue.  It would
  help to move 'start' into the constructor.

- The heartbeater has an `_operational_lock`.

  It protects `_stop_event` and `_thread`.  It could be avoided by
  combining `start` with the constructor.  `stop` is already
  idempotent.

- The leaser has an `_operational_lock` for `start` and `stop`.  See
  remarks for the heartbeater.

  The leaser has an `_add_remove_lock` to protect its leased messages,
  which represent shared mutable state.  This is used in `add` and
  `remove`, which may be called from other threads, typically the
  manager and dispatcher.  The lock could be avoided by getting add
  and remove requests via a queue that it serviced first when it woke
  up.

- The manager has 3 locks:

  `_closing`
    Used to protect the `_shutdown` method.  But the `_shutdown`
    method is the thread target of a thread started by `close`.  If
    `close` is called multiple times, multiple threads are started.

    Why don't we protect in `close`? Or in the future?

  `_pause_resume_lock`
    This protects message management, including the management of
    messages on hold.  It also manages decisions about whether to
    pause and resume the consumer.

    Shared mutable state: the on-hold structure and the leaser size.

  `_ack_deadline_lock`
    We could get rid of this if we moved the management of the ack
    deadline to the leaser.

Some ideas for simplification and getting rid of shared mutable state
---------------------------------------------------------------------

- Have a dedicated actor for managing load and pausing/restarting the
  consumer.

  It gets received/finished messages.

- Have a dedicated actor for handling ordered messages. (Don't queue
  unordered messages.)

  It gets message-finished events as well as message-received events.

- Make the leaser an actor and move deadline-management there.

- Make the dispatcher an actor by only communicating via it's queue.

Generally, whenever logic is spread over multiple components -- stop
doing that.
