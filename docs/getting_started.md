## Installation

Install using pip:
``` sh
pip install contactsoftware-functions
```

## Build your first Function

### File structure

A minimal Function implementation consists of three files:

- `environment.yaml` describes the environment and the Functions contained in it
- `requirements.txt` contains the dependencies of your Functions (usually only contactsoftware-functions)
- `mymodule.py` a Python file containing the code of your Functions (feel free to pick a different name)

Here is the complete structure:

``` bash
  my_example_environment/
  ├── environment.yaml
  ├── mymodule.py
  └── requirements.txt
```

### Function Code
Start by writing the code for your first Function. As an example we will write a Function that sends released Documents to an ERP system.

``` python title="mymodule.py"

from csfunctions import MetaData, Service
from csfunctions.events import DocumentReleaseEvent

def send_doc_to_erp(metadata: MetaData, event: DocumentReleaseEvent, service: Service):
  ...
```

While you don't have to use type annotations, it is highly recommended because it enables autocomplete in your IDE and helps you spot mistakes faster.
For our example we only need the [DocumentReleaseEvent](reference/events.md/#documentreleaseevent). It contains a list of documents that were released. Typically this will only be a single document, however it is best practices to iterate over all of the documents.

``` python title="mymodule.py"
import requests
import json

from csfunctions import MetaData, Service
from csfunctions.events import DocumentReleaseEvent

def send_doc_to_erp(metadata: MetaData, event: DocumentReleaseEvent, service: Service):
  # iterate over the documents contained in the event
  for document in event.data.documents:
    # create the payload for our (fictional ERP system)
    payload = json.dumps({
      "document_number": document.z_nummer,
      "document_index": document.z_index,
      "document_title": document.titel
    })
    res = requests.post("https://example.com", data=payload)
    if res.status_code != 200:
      return ValueError(f"Failed to upload document to ERP. Got response code {res.status_code}")

```

Here we send a payload, containing a few attributes from the released document, to [example.com](https://example.com). This is just for illustration purposes!
Please refer to the documentation of your ERP system on how the request needs to be formatted and which endpoint and credentials to use.

### Register the Function

The Function needs to be registered in the `environment.yaml`:


``` yaml title="environment.yaml"
runtime: python3.10
version: v1
functions:
  - name: send_doc_to_erp
    entrypoint: mymodule.send_doc_to_erp
```

You can add as many functions to the list as you like. The function `name` can be picked freely and doesn't have to match the name of your Python method (although it is recommended that it does). The name will be used to identify the Function in you CIM Database Cloud instance. The `entrypoint` needs to be the import path of your Python function.


### Dependencies
Lastly define your codes dependencies in the `requirements.txt`:

``` python title="requirements.txt"
contactsoftware-functions
```
contactsoftware-functions will always need to be in the requirements.txt unless you register your own main_entrypoint (see [Python runtime](reference/runtime.md)).


### Deploy the Code
To deploy the Code you first need to install the [contactsoftware-functions-client](https://pypi.org/project/contactsoftware-functions-client/) and retrieve developer credentials in the CONTACT Portal.

Install client:

```bash
pip install contactsoftware-functions-client
```

Login:

```bash
cfc login
```

Create a new environment:

```bash
cfc env create myenv
```

Upload code into new environment:

```bash
cfc env deploy myenv
```

### Test the Function
To test your Function you need to connect the Function to an event in your CIM Database Cloud instance.
Please refer to the Webhooks CIM Database Cloud documentation on how to do that.
