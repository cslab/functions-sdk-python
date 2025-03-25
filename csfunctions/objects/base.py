from enum import Enum
from typing import TYPE_CHECKING, Hashable

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from csfunctions.events import EventData


class ObjectType(str, Enum):
    DOCUMENT = "document"
    CAD_DOCUMENT = "cad_document"
    PART = "part"
    FILE = "file"
    ENGINEERING_CHANGE = "engineering_change"
    MATERIAL = "material"
    BOM_ITEM = "bom_item"
    OBJECT_PROPERTY_VALUE = "object_property_value"
    WORKFLOW = "workflow"
    BRIEFCASE = "briefcase"
    PERSON = "person"


class BaseObject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    object_type: ObjectType

    def __eq__(self, other):
        """
        Compare only the hashable fields of the model.
        """
        if not isinstance(other, self.__class__):
            return False

        # Get hashable fields, excluding non-hashable types
        hashable_fields = {k: v for k, v in self.model_dump().items() if isinstance(v, Hashable)}

        # Compare hashable fields
        return hashable_fields == {k: v for k, v in other.model_dump().items() if isinstance(v, Hashable)}

    def link_objects(self, data: "EventData"):  # pylint: disable=unused-argument
        """
        Create a link between this object and related objects in data, so that we can access them through dot notation.
        E.g. we want to be able to access 'document.part'.
        The event data needs to contain all objects as list fields, e.g. data.parts: list[Part].
        """
        return
