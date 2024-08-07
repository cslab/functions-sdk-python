from typing import List, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


def get_items_of_type(model: BaseModel, target_type: Type[T]) -> List[T]:
    """
    Retrieve items of a specific type from lists within a Pydantic model.

    This is useful, e.g. to get all Documents or Parts from an events data package,
    without having to know how the fields are called.

    Args:
        model (BaseModel): The Pydantic model to search through.
        target_type (Type[T]): The type of items to search for.

    Returns:
        List[T]: A list of items of the specified type found within lists in the model.
    """
    items = []
    for field_name in model.model_fields_set:
        attr = getattr(model, field_name)
        if isinstance(attr, list):
            for item in attr:
                if isinstance(item, target_type):
                    items.append(item)
    return items
