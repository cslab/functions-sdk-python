from unittest import TestCase

from csfunctions import Request
from tests.utils import dummy_request

SINGLE_DATA = {
    "scheme_updates": {"{obj.name}": [True]},
    "ctx": {"action": "create"},
    "obj": {"name": "test"},
    "old_cfv_str": "",
    "matches": [["", "{obj.name}"]],
    "prefix": "cfv_part_teilenummer_",
}


def _request(data: dict) -> Request:
    # parsed from plain JSON data like the handler does
    return Request.model_validate(
        {
            "metadata": dummy_request.metadata.model_dump(),
            "event": {"name": "field_value_calculation", "event_id": "123", "data": data},
        }
    )


class TestFieldValueCalculation(TestCase):
    def test_single_calculation(self):
        # requests without calculations (sent by older backends) are still accepted
        request = _request(SINGLE_DATA)
        self.assertIsNone(request.event.data.calculations)
        self.assertEqual("cfv_part_teilenummer_", request.event.data.prefix)

    def test_several_calculations(self):
        calculations = [
            {
                "sid": f"cssaas.vp_cad/calculated-field/{attribute}",
                "attribute": attribute,
                "scheme_updates": {"{obj.name}": [True]},
                "old_cfv_str": "",
                "matches": [["", "{obj.name}"]],
                "prefix": f"cfv_part_{attribute}_",
            }
            for attribute in ("teilenummer", "benennung")
        ]
        request = _request(SINGLE_DATA | {"calculations": calculations})

        parsed = request.event.data.calculations
        self.assertEqual(["teilenummer", "benennung"], [c.attribute for c in parsed])
        self.assertEqual("cfv_part_benennung_", parsed[1].prefix)

    def test_attribute_types(self):
        # older backends don't send attribute_types
        self.assertEqual({}, _request(SINGLE_DATA).event.data.attribute_types)

        attribute_types = {"cdb_cdate": "date", "cca_integer_doc_1": "int", "Item.cdb_cdate": "date"}
        request = _request(SINGLE_DATA | {"attribute_types": attribute_types})
        self.assertEqual(attribute_types, request.event.data.attribute_types)

        with self.assertRaises(ValueError):
            _request(SINGLE_DATA | {"attribute_types": {"cca_bool": "bool"}})
