from copy import deepcopy
from unittest import TestCase

from .utils import dummy_document, dummy_part


class TestObject(TestCase):
    def test_equals(self):
        doc1 = deepcopy(dummy_document)
        doc1.part = dummy_part
        doc1_copy = deepcopy(dummy_document)

        doc2 = deepcopy(dummy_document)
        doc2.z_index = "b"
        doc2.part = dummy_part

        self.assertEqual(doc1, doc1_copy)
        self.assertNotEqual(doc1, doc2)
        self.assertNotEqual(doc1_copy, doc2)
        self.assertEqual(doc1, doc1)
