from typing import Annotated, Union

from pydantic import Field

from .base import BaseObject
from .briefcase import Briefcase
from .classification import ObjectPropertyValue
from .document import CADDocument, Document
from .engineering_change import EngineeringChange
from .file import File
from .part import BOMItem, Material, Part
from .person import Person
from .workflow import Workflow

Object = Annotated[
    Union[
        Document,
        CADDocument,
        Part,
        File,
        EngineeringChange,
        Material,
        BOMItem,
        ObjectPropertyValue,
        Briefcase,
        Workflow,
        Person,
    ],
    Field(discriminator="object_type"),
]


__all__ = [
    "Document",
    "CADDocument",
    "Part",
    "File",
    "EngineeringChange",
    "Material",
    "BOMItem",
    "ObjectPropertyValue",
    "Briefcase",
    "Workflow",
    "BaseObject",
    "Person",
]
