import threading
from typing import Optional, Iterable
import copy
import typing
import datetime
import itertools

if typing.TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.pubsub_v1.subscriber._protocol.streaming_pull_manager import (
        StreamingPullManager,
    )

_INITIAL_MODACK_SLEEP_DURATION = 0.1
_LEASE_WORKER_NAME = "Thread-InitialModAck"

class InitialModack(object):
    def __init__(self, manager: "StreamingPullManager"):
        self._thread: Optional[threading.Thread] = None
        self._manager = manager
        
        # a lock used for start/stop operations, protecting the _thread attribute
        self._operational_lock = threading.Lock()
        
        self._pending_initial_modacks = iter(())
        
        # A lock ensuring that add/remove operations are atomic and cannot be
        # intertwined. Protects _pending_initial_modacks
        self._add_remove_lock = threading.Lock()
        
        self._stop_event = threading.Event()
    
        
    def add(self, ack_ids) -> None:
        with self._add_remove_lock:
            self._pending_initial_modacks = itertools.chain(self._pending_initial_modacks, ack_ids)
        
        
    def modack(self) -> None:
        #print(f"mk: initial_modack.modack() called at {datetime.datetime.now()}")
        while not self._stop_event.is_set():
            
            with self._add_remove_lock:
                copy_pending_initial_modacks = itertools.chain(iter(()), self._pending_initial_modacks)
                self._pending_initial_modacks = iter(())
                #print(f"mk: initial_modack.modack() self._pending_initial_modacks: {list(self._pending_initial_modacks)}")
                
            self._manager._send_lease_modacks(
                copy_pending_initial_modacks, self._manager.ack_deadline, warn_on_invalid=False
            )
            
            self._stop_event.wait(timeout=_INITIAL_MODACK_SLEEP_DURATION)
    
            
    def start(self) -> None:
        with self._operational_lock:
            if self._thread is not None:
                raise ValueError("InitialModack is already running.")

            # Create and start the helper thread.
            self._stop_event.clear()
            thread = threading.Thread(
                name=_LEASE_WORKER_NAME, target=self.modack
            )
            thread.daemon = True
            thread.start()
            #print("mk: initial_modack.start(): initial_modack thread started")
            self._thread = thread
            
            
    def stop(self) -> None:
        with self._operational_lock:
            self._stop_event.set()

            if self._thread is not None:
                # The thread should automatically exit when the consumer is
                # inactive.
                self._thread.join()

            #print("mk: initial_modack.stop(): initial_modack thread stopped")
            self._thread = None