# Functions-SDK for Python

This SDK provides the **csfunctions** library for developing Functions with Python.

Functions are deeply integrated with the [CIM Database Cloud](https://www.cim-database-cloud.com){:target="_blank"} Webhooks technology. They are designed to work seamlessly together. The goal is to allow you to implement custom business logic in a CIM Database Cloud SaaS application without leaving CONTACT Cloud and without the need to create and maintain separate infrastructure.

## Requirements

Python 3.10+

csfunctions is built with [Pydantic 2](https://docs.pydantic.dev/latest/){:target="_blank"}.

## Installation
Install using pip:
```bash
pip install contactsoftware-functions
```
## Usage
### Build the Function

Folder contents of a minimal example for a Function implementation:

```bash
  my_example_functions/
  ├── environment.yaml
  ├── mymodule.py
  └── requirements.txt
```


Code for a Function:

```python title="mymodule.py"
import requests
import json

from csfunctions import MetaData, Service
from csfunctions.events import DocumentReleaseEvent

def send_doc_to_erp(metadata: MetaData, event: DocumentReleaseEvent, service: Service):
  # Iterate over the documents contained in the event
  for document in event.data.documents:
    # Create the payload for our (fictional ERP system)
    payload = json.dumps({
      "document_number": document.z_nummer,
      "document_index": document.z_index,
      "document_title": document.titel
    })
    res = requests.post("https://example.com", data=payload)
    if res.status_code != 200:
      return ValueError(f"Failed to upload document to ERP. Got response code {res.status_code}")

```

Environment file to define runtime and Function entry points:

```yaml title="environment.yaml"
runtime: python3.10
version: v1
functions:
  - name: send_doc_to_erp
    entrypoint: mymodule.send_doc_to_erp
```


Define requirements:

```python title="requirements.txt"
contactsoftware-functions
```

### Deploy the Code
To deploy the code, you first need to install the [contactsoftware-functions-client](https://pypi.org/project/contactsoftware-functions-client/){:target="_blank"} and retrieve developer credentials in the CONTACT Portal.

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

Upload code into the new environment:

```bash
cfc env deploy myenv
```
