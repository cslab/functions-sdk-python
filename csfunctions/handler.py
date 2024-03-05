import json
import os
import sys
import traceback
from importlib import import_module
from typing import Callable

import yaml
from pydantic import BaseModel

from csfunctions import ErrorResponse, Event, Request
from csfunctions.config import ConfigModel, FunctionModel
from csfunctions.logging import RedirectToLoki, Stream
from csfunctions.objects.base import BaseObject
from csfunctions.response import ResponseUnion
from csfunctions.service import Service

_log_stream = Stream()


def _load_config(function_dir) -> ConfigModel:
    path = os.path.join(function_dir, "environment.yaml")
    if not os.path.exists(path):
        raise OSError(f"environment file {path} does not exist")

    with open(path, "rb") as config_file:
        config = ConfigModel(**yaml.safe_load(config_file))

    return config


def _get_function(function_name: str, function_dir: str) -> FunctionModel:
    config = _load_config(function_dir)
    func = next(func for func in config.functions if func.name == function_name)
    if not func:
        raise ValueError(f"Could not find function with name { function_name} in the environment.yaml.")
    return func


def get_function_callable(function_name: str, function_dir: str) -> Callable:
    """
    Loads the function and returns the callable.
    The function needs to be configured in the environment.yaml, or else a ValueError is raised.
    """
    func = _get_function(function_name, function_dir)
    module, function_name = func.entrypoint.rsplit(".", 1)
    sys.path.insert(0, function_dir)
    mod = import_module(module, "")
    return getattr(mod, function_name)


def link_documents2parts(event: Event) -> None:
    """
    Links the relationship document -> part
    """
    if hasattr(event.data, "documents") and hasattr(event.data, "parts"):
        # build parts dicts, indexed by teilenummer@index
        parts = {}
        for part in event.data.parts:
            key = part.teilenummer + "@" + part.t_index
            parts[key] = part

        # link the parts to the documents
        for document in event.data.documents:
            if document.teilenummer is None or document.t_index is None:
                continue
            key = document.teilenummer + "@" + document.t_index
            if key in parts:
                document.part = parts[key]


def link_objects(event: Event):
    """
    Link the relationships between objects, to allow accessing relationships with dot notation,
    e.g. document.part
    """
    data = getattr(event, "data", None)
    if not isinstance(data, BaseModel):
        return

    # we expect all objects to be passed in Event.data
    # e.g. all parts would be in Event.data.parts = list[Part]

    for field_name in data.model_fields_set:
        # go through each field in data and look for fields that are lists
        # objects will always be passed in a list

        field = getattr(data, field_name)
        if isinstance(field, list):
            for obj in field:
                # the list might contain entries that are not objects, so we check first
                if isinstance(obj, BaseObject):
                    obj.link_objects(data)


def execute(function_name: str, request_body: str, function_dir: str = "src") -> str:
    """
    This is the main entrypoint that gets called by default when the function is executed in AWS lambda.
    It tries to load the requested function, executes the function and returns the result.
    Functions need to be configured in the environment.yaml and accept two parameters: 'metadata' and 'event'
    The request_body should be a json encoded string containing the request (event and metadata).
    """
    try:
        request = Request(**json.loads(request_body))
        link_objects(request.event)
        function_callback = get_function_callable(function_name, function_dir)
        service = Service(str(request.metadata.service_url), request.metadata.service_token)

        with RedirectToLoki(_log_stream, request.event.event_id):
            result = function_callback(request.metadata, request.event, service)

        if not isinstance(
            result, ResponseUnion
        ):  # need to check for ResponseUnion instead of Response, because isinstance doesn't work with annotated unions
            raise ValueError("Function needs to return a Response object.")
    except Exception as e:  # pylint: disable=broad-except
        result = ErrorResponse(message=str(e), error_type=type(e).__name__, trace=traceback.format_exc(), id="")

    return result.model_dump_json()
