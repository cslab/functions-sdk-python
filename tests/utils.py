from datetime import datetime

from csfunctions import DataResponse, MetaData, Request, Service
from csfunctions.actions import AbortAndShowErrorAction
from csfunctions.events import DummyEvent
from csfunctions.events.dummy import DummyEventData
from csfunctions.objects import Document, EngineeringChange, Part


def ping_function(metadata: MetaData, event: DummyEvent, _: Service):
    """
    Test function for testing function execution.
    The function pings back the received request as data.
    """
    return DataResponse(data={"metadata": metadata.model_dump(), "event": event.model_dump()}, event_id="123")


def empty_function(*args, **kwargs):  # pylint: disable=unused-argument
    """
    An empty function that doesn't do anything.
    """
    pass  # pylint: disable=unnecessary-pass


def action_function(*args, **kwargs):  # pylint: disable=unused-argument
    """
    A Function that returns an Action
    """
    return AbortAndShowErrorAction(message="Testerror")


def action_list_function(*args, **kwargs):  # pylint: disable=unused-argument
    """
    A Function that returns a list of  Actions
    """
    return [AbortAndShowErrorAction(message="Testerror"), AbortAndShowErrorAction(message="Testerror")]


dummy_document = Document.model_validate(
    {
        "object_type": "document",
        "z_nummer": "D000017",
        "z_index": "a",
        "titel": "aa",
        "category1_name_en": "Electrical / Electronic Engineering",
        "category1_name_de": "E-Technik / Elektronik",
        "category2_name_en": "Circuit Diagram",
        "category2_name_de": "Stromlaufplan",
        "z_categ1": "312",
        "z_categ2": "393",
        "cdb_obsolete": 0,
        "z_status": 0,
        "z_status_txt": "Draft",
        "autoren": "Administrator",
        "z_bereich": "IT",
        "z_language": "",
        "keywords": "test",
        "z_bemerkung": "",
        "joined_status_name": "Draft",
        "erzeug_system": "-",
        "cdb_lock": "",
        "ce_valid_from": "9999-12-31T00:00:00",
        "ce_valid_to": None,
        "cdb_ec_id": "",
        "ursprungs_z": "",
        "teilenummer": "000000",
        "t_index": "a",
        "cdb_project_id": "",
        "project_name": "",
        "src_name": "",
        "src_cdate": None,
        "src_rdate": None,
        "src_number": "",
        "src_index": "",
        "src_fname": "",
        "source_oid": "",
        "cdb_cpersno": "caddok",
        "mapped_cdb_cpersno_name": "Administrator",
        "cdb_cdate": "2023-01-25T12:44:04",
        "cdb_mpersno": "caddok",
        "mapped_cdb_mpersno_name": "Administrator",
        "cdb_mdate": "2023-01-25T12:50:16",
        "cdb_m2persno": "",
        "mapped_cdb_m2persno_name": "",
        "cdb_m2date": None,
        "part": None,
    }
)

dummy_part = Part.model_validate(
    {
        "object_type": "part",
        "teilenummer": "000000",
        "t_index": "a",
        "status": 0,
        "materialnr_erp": "000000",
        "benennung": "",
        "eng_benennung": "test",
        "benennung2": "",
        "t_kategorie_name_de": "Baugruppe Fremdbezug",
        "t_kategorie_name_en": "External Assembly",
        "cdb_t_project_id": "",
        "t_bereich": "IT",
        "cdb_t_ec_id": "",
        "item_maturity": 10,
        "gebrauchsstand_name_de": "Aktiv",
        "gebrauchsstand_name_en": "Active",
        "ce_valid_from": "9999-12-31",
        "ce_valid_to": None,
        "mengeneinheit_name_de": "kg",
        "mengeneinheit_name_en": "kg",
        "st_gewicht": 0.0,
        "material_object_id": "",
        "surface_name_en": "",
        "surface_name_de": "",
        "techdaten": "",
        "cssaas_mirrored_from": "",
        "t_ersatz_fuer": "",
        "t_ersatz_durch": "",
        "din": "",
        "bemerkung": "",
        "cdb_copy_of_item_id": "",
        "type_object_id": "af664278-1938-11eb-9e9d-10e7c6454cd1",
        "cdb_depends_on": "",
        "site_object_id": "",
        "cssaas_frame_add_attr_1": "",
        "cssaas_frame_add_attr_2": "",
        "cssaas_frame_add_attr_3": "",
        "cssaas_frame_add_attr_4": "",
        "cssaas_frame_add_attr_5": "",
        "cdb_cpersno": "caddok",
        "cdb_cpersno_name": "Administrator",
        "cdb_cdate": "2023-07-03T10:07:49",
        "cdb_mpersno": "caddok",
        "cdb_mpersno_name": "Administrator",
        "cdb_mdate": "2023-07-03T10:07:49",
        "cdb_m2persno": "",
        "cdb_m2persno_name": "",
        "cdb_m2date": None,
    }
)

dummy_request = Request(
    metadata=MetaData.model_validate(
        {
            "request_id": "123",
            "app_lang": "de",
            "app_user": "caddok",
            "request_datetime": datetime(2000, 1, 1),
            "transaction_id": "123asd",
            "instance_url": "https://instance.contact-cloud.com",
            "service_url": None,
            "service_token": "123",
            "db_service_url": None,
        }
    ),
    event=DummyEvent(event_id="42", data=DummyEventData(documents=[dummy_document], parts=[dummy_part])),
)


dummy_ec = EngineeringChange.model_validate(
    {
        "object_type": "engineering_change",
        "cdb_ec_id": "EC00000005",
        "cdb_project_id": "",
        "ec_state": "ECN",
        "end_time_plan": "2024-01-09T23:00:00",
        "status": 100,
        "title": "testEC",
        "template_ec_id": "EC00000000",
        "c_department": "",
        "c_description": "",
        "c_event": "Kostenminimierung",
        "c_reason": "Stuff is too expensive!",
        "c_source": "Kunde",
        "category": "Standard",
        "part_ids": ["000000@a"],
        "document_ids": ["D000017@a"],
        "planned_changes_part_ids": ["000000@a"],
        "planned_changes_document_ids": ["D000017@a"],
        "cdb_cpersno": "caddok",
        "cdb_cdate": "2024-01-09T11:11:33",
        "cdb_mpersno": "caddok",
        "cdb_mdate": "2024-01-09T11:40:20",
    }
)
