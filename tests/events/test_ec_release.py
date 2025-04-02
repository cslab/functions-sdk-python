from copy import deepcopy
from unittest import TestCase

from csfunctions.events import EngineeringChangeReleasedData, EngineeringChangeReleasedEvent
from csfunctions.handler import link_objects
from tests.utils import dummy_document, dummy_ec, dummy_part, dummy_request


class TestECRelease(TestCase):
    def test_link_objects(self):
        # deepcopy the dummy objects, because link_objects would modify them
        document = deepcopy(dummy_document)
        part = deepcopy(dummy_part)
        engineering_change = deepcopy(dummy_ec)

        request = dummy_request

        data = EngineeringChangeReleasedData(
            documents=[document], parts=[part], engineering_changes=[engineering_change]
        )
        event = EngineeringChangeReleasedEvent(event_id="123", data=data)
        request.event = event

        # objects are not linked yet
        self.assertIsNone(document.part)
        self.assertEqual(0, len(engineering_change.parts))
        self.assertEqual(0, len(engineering_change.planned_changes_parts))
        self.assertEqual(0, len(engineering_change.documents))
        self.assertEqual(0, len(engineering_change.planned_changes_documents))

        link_objects(request.event)

        # now they are
        self.assertIsNotNone(document.part)
        self.assertEqual(1, len(engineering_change.parts))
        self.assertEqual(1, len(engineering_change.planned_changes_parts))
        self.assertEqual(1, len(engineering_change.documents))
        self.assertEqual(1, len(engineering_change.planned_changes_documents))

        # nested linked objects
        self.assertEqual(part, engineering_change.documents[0].part)
