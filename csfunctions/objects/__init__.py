from typing import Annotated, Union

from pydantic import Field

from .briefcase import Briefcase
from .classification import ObjectPropertyValue
from .document import CADDocument, Document
from .engineering_change import EngineeringChange
from .file import File
from .part import BOMItem, Material, Part
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
    ],
    Field(discriminator="object_type"),
]
