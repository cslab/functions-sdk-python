This section is aimed at developers that want to build their own Functions-SDK.
If you are building Functions with **csfunctions** you can skip this part.

## Architecture
Function environment are docker containers that run in AWS-lambda. The Python runtime utilizes awslambdaric to handle the requests. The Python runtime is part of the CIM Database Cloud Functions infrastructure and currently cannot be customized.


## Lambda "execute" Function request
When a Webhook is calling a Function the following request body will be sent to the endpoint of the Lambda-Function:
```json
{
    "request": "execute",
    "function" : "my_function",
    "payload" : "{... json encoded payload}"
}
```

This request is then processed by the Python runtimes dispatcher. The dispatcher calls the execute handler `csfunctions.handler.execute`. If you don't want to use **csfunctions** you need to implement your own execute handler and register your custom handler in the `environment.yaml` config file as `main_entrypoint`.

``` yaml title="environment.yaml"
runtime: python3.10
version: v1
main_entrypoint: mymodule.execute  // register a custom execute handler here
functions:
  - name: myfunc
    entrypoint: mymodule.myfunc
```

The signature of your custom `execute` method needs to look like this:
```python
def execute(
  function_name: str,
  request_body: str
  ) -> str:
```

The return value of the execute method is the json encoded response payload.

## Payloads

The Request and response payloads are described in the CIM Database Cloud documentation. The [functions-sdk-python](https://github.com/cslab/functions-sdk-python){:target="_blank"} GitHub repository also contains the complete [JSON-schema files](https://github.com/cslab/functions-sdk-python/tree/main/json_schemas){:target="_blank"}.
