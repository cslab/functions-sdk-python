"""
The development server looks for an environment.yaml in the given directory and reads the Functions from it.
The Functions are then available via HTTP requests to the server.

The server will automatically restart if you make changes to your Functions code or to the `environment.yaml` file.

Usage:

```bash
python -m csfunctions.devserver
```

Optional arguments:

--dir <directory>
    The directory containing the environment.yaml file.
    (default: current working directory)

--secret <secret>
    The secret token to use for the development server.

--port <port>
    The port to run the development server on.
    (default: 8000)

--no-reload
    Disable auto reloading of the server.
"""

import argparse
import hashlib
import hmac
import json
import logging
import os
import time
from collections.abc import Iterable

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


def _verify_hmac_signature(
    signature: str | None, timestamp: str | None, body: str, secret_token: str, max_age: int = 60
) -> bool:
    """
    Verify the HMAC signature of the request.
    If timestamp is older than max_age seconds, the request is rejected. (default: 60 seconds, disable with -1)
    """
    if not secret_token:
        # this should not happen, since this function should only be called if a secret token is set
        raise ValueError("Missing secret token")

    if not signature:
        logging.warning("Request does not contain a signature")
        return False

    if not timestamp:
        logging.warning("Request does not contain a timestamp")
        return False

    if max_age >= 0 and int(timestamp) < time.time() - max_age:
        logging.warning("Timestamp of request is older than %d seconds", max_age)
        return False

    return hmac.compare_digest(
        signature,
        hmac.new(
            secret_token.encode("utf-8"),
            f"{timestamp}{body}".encode(),
            hashlib.sha256,
        ).hexdigest(),
    )


def handle_request(request: Request) -> Response:
    """
    Handles a request to the development server.
    Extracts the function name from the request path and executes the Function using the execute handler.
    """
    function_name = request.path.strip("/")
    if not function_name:
        return Response("No function name provided", status=400)
    body = request.get_data(as_text=True)
    signature = request.headers.get("X-CON-Signature-256")
    timestamp = request.headers.get("X-CON-Timestamp")

    secret_token = os.environ.get("CON_DEV_SECRET", "")
    if secret_token and not _verify_hmac_signature(signature, timestamp, body, secret_token):
        return Response("Invalid signature", status=401)

    try:
        function_dir = os.environ.get("CON_DEV_DIR", "")
        logging.info("Executing function: %s", function_name)
        response = execute(function_name, body, function_dir=function_dir)
    except FunctionNotRegistered as e:
        logging.warning("Function not found: %s", function_name)
        return Response(str(e), status=404)

    if _is_error_response(response):
        logging.error("Function %s returned error response", function_name)
        return Response(response, status=500, content_type="application/json")

    return Response(response, content_type="application/json")


def application(environ, start_response) -> Iterable[bytes]:
    request = Request(environ)
    response = handle_request(request)
    return response(environ, start_response)


def run_server() -> None:
    port = int(os.environ.get("CON_DEV_PORT", 8000))
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port number: {port}")

    logging.info("Starting development server on port %d", port)
    # B104: binding to all interfaces is intentional - this is a development server
    run_simple(
        "0.0.0.0",  # nosec: B104
        port,
        application,
        use_reloader=not bool(os.environ.get("CON_DEV_NO_RELOAD")),
        extra_files=[os.path.join(os.environ.get("CON_DEV_DIR", ""), "environment.yaml")],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        help="The directory containing the environment.yaml file. (default: current working directory)",
    )
    parser.add_argument(
        "--secret",
        type=str,
        help="The secret token to use for the development server.",
    )
    parser.add_argument("--port", type=int, help="The port to run the development server on. (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto reloading of the server.")
    args = parser.parse_args()

    # Command line arguments take precedence over environment variables
    if args.dir:
        os.environ["CON_DEV_DIR"] = args.dir
    if args.secret:
        os.environ["CON_DEV_SECRET"] = args.secret
    if args.port:
        os.environ["CON_DEV_PORT"] = str(args.port)
    if args.no_reload:
        os.environ["CON_DEV_NO_RELOAD"] = "1"

    if not os.environ.get("CON_DEV_SECRET"):
        logging.warning(
            "\033[91m\033[1mNo secret token provided, development server is not secured!"
            " It is recommended to provide a secret via --secret <secret> to"
            " enable HMAC validation.\033[0m"
        )

    run_server()
