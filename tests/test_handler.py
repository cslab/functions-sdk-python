import json
import os
from copy import deepcopy
from unittest import TestCase

from csfunctions.handler import execute, get_function_callable, link_objects
from tests.utils import dummy_request, ping_function


class TestHandler(TestCase):
    def setUp(self) -> None:
        self.source_dir = os.path.join(os.path.dirname(__file__), "..")
        with open(os.path.join(self.source_dir, "environment.yaml"), "w", encoding="utf-8") as f:
            f.write(
                """runtime: python3_10
version: v1
functions:
  - name: dummy
    entrypoint: main.main
  - name: ping
    entrypoint: tests.utils.ping_function
  - name: empty
    entrypoint: tests.utils.empty_function
"""
            )

    def tearDown(self) -> None:
        os.remove(os.path.join(self.source_dir, "environment.yaml"))

    def test_get_function_callback(self):
        func = get_function_callable("ping", self.source_dir)
        self.assertEqual(ping_function.__name__, func.__name__)

    def test_execute(self):
        request = deepcopy(dummy_request)  # make a deepcopy, since request object will be modified by link_objects
        result = execute("ping", json.dumps(request.model_dump(mode="json"), separators=(",", ":")), self.source_dir)
        # we need to add separators=(',', ':'), to make sure there are no whitespaces
        # between assignments like "key":_"value"
        link_objects(request.event)
        expected = {
            "response_type": "data",
            "event_id": request.event.event_id,
            "data": {
                "metadata": request.metadata.model_dump(mode="json"),
                "event": request.event.model_dump(mode="json"),
            },
        }
        self.assertEqual(json.dumps(expected, separators=(",", ":")), result)

        # test empty function
        request = deepcopy(dummy_request)  # make a deepcopy, since request object will be modified by link_objects
        result = execute("empty", json.dumps(request.model_dump(mode="json"), separators=(",", ":")), self.source_dir)
        self.assertEqual("", result)

    def test_link_objects(self):
        request = deepcopy(dummy_request)  # make a deepcopy, since request object will be modified by link_objects

        link_objects(request.event)

        # part can be access with dot notation on the document
        self.assertIsNotNone(request.event.data.documents[0].part)
        self.assertEqual(request.event.data.documents[0].part, request.event.data.parts[0])
        self.assertEqual(request.event.data.documents[0].teilenummer, request.event.data.documents[0].part.teilenummer)
        self.assertEqual(request.event.data.documents[0].t_index, request.event.data.documents[0].part.t_index)
