"""
The development server looks for an environment.yaml in the current working directory and reads the Functions from it.
The Functions are then available via HTTP requests to the server.

"""

import argparse
import json

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from csfunctions.handler import FunctionNotRegistered, execute


def _is_error_response(function_response: str | dict):
    """
    Try to figure out if the response from the function is an error response.
    This is the same implementation as in the runtime, to ensure the behavior is the same.
    """
    if isinstance(function_response, str):
        # function response could be a json encoded dict, so we try to decode it first
        try:
            function_response = json.loads(function_response)
        except json.JSONDecodeError:
            # response is not json decoded, so it's not an error response
            return False

    if isinstance(function_response, dict):
        # check if the response dict is an error response
        return function_response.get("response_type") == "error"
    else:
        # function response is neither a dict nor json encoded dict, so can't be an error response
        return False


def handle_request(request: Request, function_dir: str = "") -> Response:
    """
    Handles a request to the development server.
    Extracts the function name from the request path and executes the Function using the execute handler.
    """
    function_name = request.path.strip("/")
    if not function_name:
        return Response("No function name provided", status=400)
    body = request.get_data(as_text=True)

    try:
        # we assume the function is in the current working directory
        response = execute(function_name, body, function_dir=function_dir)
    except FunctionNotRegistered as e:
        return Response(str(e), status=404)

    if _is_error_response(response):
        # If a Function raises an error the execute handler will wrap the error in an ErrorResponse
        # We need to check for that to return the correct status code.
        return Response(response, status=500, content_type="application/json")

    return Response(response, content_type="application/json")


def create_application(function_dir: str = ""):
    def application(environ, start_response):
        request = Request(environ)
        response = handle_request(request, function_dir=function_dir)
        return response(environ, start_response)

    return application


def run_server(function_dir: str = ""):
    # B104: binding to all interfaces is intentional - this is a development server
    run_simple("0.0.0.0", 8000, create_application(function_dir=function_dir), use_reloader=True)  # nosec: B104


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="", help="The directory containing the environment.yaml file")
    args = parser.parse_args()
    run_server(function_dir=args.dir)
