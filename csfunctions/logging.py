import contextlib
import json
import os
import queue
import threading
import time

import requests


class Stream:
    def __init__(self):
        self.queue = None
        self._msg = ""

    def write(self, message):
        if self.queue is None:
            raise ValueError("Queue is None")

        for char in message:
            if char in ("\n", "\r"):
                self.queue.put((time.time_ns(), self._msg))
                self._msg = ""
            else:
                self._msg += char

    def flush(self):
        pass


class RedirectToLoki:  # pylint: disable=too-many-instance-attributes
    def __init__(self, stream: Stream, event_id: str):
        self.queue = queue.Queue(-1)
        stream.queue = self.queue

        self._thread = None
        self.stream = stream

        self.loki_session = None

        self.headers = {"X-Scope-OrgID": os.getenv("LOKI_TENANT")}
        self.event_id = event_id
        self.environment = os.getenv("ENVIRONMENT_NAME")
        self.customer_id = os.getenv("CUSTOMER_ID")

        self.context_stdout = contextlib.redirect_stdout(self.stream)
        self.context_stderr = contextlib.redirect_stderr(self.stream)

    def __enter__(self):
        # redirect streams
        self.context_stdout.__enter__()
        self.context_stderr.__enter__()

        # create http session
        self.loki_session = requests.Session()

        # start thread to consume stream queue and push to loki
        self._thread = threading.Thread(target=self._monitor)
        self._thread.daemon = True
        self._thread.start()

    def __exit__(self, _type, value, traceback):
        # put close marker into queue
        self.queue.put(None)

        # wait for all entries to be processed, then close thread and session
        self._thread.join()
        self._thread = None
        self.loki_session.close()

        # move streams to normal
        self.context_stdout.__exit__(_type, value, traceback)
        self.context_stderr.__exit__(_type, value, traceback)

    def _monitor(self):
        """
        Monitor the queue for records
        This method runs on a separate, internal thread.
        The thread will terminate if it sees a sentinel object in the queue.
        """
        while True:
            try:
                message = self.queue.get(True)

                # close marker is "None"
                if message is None:
                    self.queue.task_done()
                    break

                self.post_log(message)
                self.queue.task_done()

            except queue.Empty:
                break

    def _prepare_message(self, timestamp_ns: int, message: str) -> dict:
        entry = {"event_id": self.event_id, "message": message, "customer_id": self.customer_id}
        data = {
            "streams": [
                {
                    "stream": {"app": "function", "environment": self.environment},
                    "values": [[str(timestamp_ns), json.dumps(entry)]],
                }
            ]
        }

        return data

    def post_log(self, message: [int, str]):
        self.loki_session.post(
            os.getenv("LOKI_URL"), json=self._prepare_message(message[0], message[1]), headers=self.headers
        )
