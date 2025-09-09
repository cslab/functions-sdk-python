import json
import logging
import os
import sys
import traceback
from functools import lru_cache
from importlib import import_module
from typing import Callable

import yaml

from csfunctions import ErrorResponse, Event, Request, WorkloadResponse
from csfunctions.actions import ActionUnion
from csfunctions.config import ConfigModel, FunctionModel
from csfunctions.events import EventData
from csfunctions.objects import BaseObject
from csfunctions.response import ResponseUnion
from csfunctions.service import Service

logger = logging.getLogger(__name__)


class FunctionNotRegistered(ValueError):
    """
    Raised when a function is not found in the environment.yaml.
    """


@lru_cache(maxsize=1)
def load_environment_config(function_dir: str) -> ConfigModel:
    path = os.path.join(function_dir, "environment.yaml")
    if not os.path.exists(path):
        raise OSError(f"environment file {path} does not exist")

    with open(path, "rb") as config_file:
        config = ConfigModel(**yaml.safe_load(config_file))

    return config


def _get_function(function_name: str, function_dir: str) -> FunctionModel:
    config = load_environment_config(function_dir)
    func = next(func for func in config.functions if func.name == function_name)
    if not func:
        raise FunctionNotRegistered(f"Could not find function with name {function_name} in the environment.yaml.")
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


def link_objects(event: Event):
    """
    Link the relationships between objects, to allow accessing relationships with dot notation,
    e.g. document.part
    """
    data = getattr(event, "data", None)
    if data is None or not isinstance(data, EventData):  # type: ignore  # MyPy doesn't like PEP604
        return

    # we expect all objects to be passed in Event.data
    # e.g. all parts would be in Event.data.parts = list[Part]

    for field_name in data.model_fields_set:
        # go through each field in data and look for fields that are lists of BaseObjects
        # or direct BaseObjects

        field = getattr(data, field_name)
        if isinstance(field, list):
            for obj in field:
                # the list might contain entries that are not objects, so we check first
                if isinstance(obj, BaseObject):
                    obj.link_objects(data)
        elif isinstance(field, BaseObject):
            field.link_objects(data)


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
        service = Service(metadata=request.metadata)

        response = function_callback(request.metadata, request.event, service)

        if response is None:
            return ""

        if isinstance(response, ActionUnion):  # type: ignore  # MyPy doesn't like PEP604
            # wrap returned Actions into a WorkloadResponse
            response = WorkloadResponse(actions=[response])
        elif isinstance(response, list) and all(isinstance(o, ActionUnion) for o in response):  # type: ignore  # MyPy doesn't like PEP604
            # wrap list of Actions into a WorkloadResponse
            response = WorkloadResponse(actions=response)

        if not isinstance(response, ResponseUnion):  # type: ignore  # MyPy doesn't like PEP604
            # need to check for ResponseUnion instead of Response, because isinstance doesn't work with annotated unions
            raise ValueError("Function needs to return a Response object or None.")

        # make sure the event_id is filled out correctly
        response.event_id = request.event.event_id

    except Exception as e:  # pylint: disable=broad-except
        logger.error("An error occurred while executing function %s", function_name, exc_info=True)
        response = ErrorResponse(message=str(e), error_type=type(e).__name__, trace=traceback.format_exc(), id="")

    return response.model_dump_json()
