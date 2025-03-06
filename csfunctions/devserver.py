"""
The development server looks for an environment.yaml in the current working directory and reads the Functions from it.
The Functions are then available via HTTP requests to the server.

"""

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from csfunctions.handler import execute


def handle_request(request: Request) -> Response:
    """
    Handles a request to the development server.
    """
    function_name = request.path.strip("/")
    if not function_name:
        return Response("No function name provided", status=400)
    body = request.get_data(as_text=True)
    response = execute(function_name, body, "src")
    return Response(response, content_type="application/json")


def application(environ, start_response):
    request = Request(environ)
    response = handle_request(request)
    return response(environ, start_response)


def run_server():
    # B104: binding to all interfaces is intentional - this is a development server
    run_simple("0.0.0.0", 8000, application, use_reloader=True)  # nosec: B104


if __name__ == "__main__":
    run_server()
