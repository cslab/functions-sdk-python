 <h1><a href="https://github.com/cslab/functions-sdk-python"><img src="https://github.com/cslab/functions-sdk-python/blob/main/docs/assets/contact-logo.svg" width="50" alt="CONTACT Logo"></a> Functions-SDK for Python</h1>

This SDK provides the **csfunctions** library for developing Functions with Python.

Functions are deeply integrated in the CIM Database Cloud Webhooks technology. They are designed to work seamlessly together. The goal is to allow implementing custom business logic in a CIM Database Cloud SaaS application without leaving the CONTACT Cloud and without the need to create and maintain a separate infrastructure.

**Documentation:** https://cslab.github.io/functions-sdk-python/

**Source code:** https://github.com/cslab/functions-sdk-python

## Requirements

Python 3.10+

csfunctions is built with [Pydantic 2](https://docs.pydantic.dev/latest/)

## Installation
Install using pip:
``` sh
pip install contactsoftware-functions
```
## Usage
### Build the Function

Folder content of a minimal example for a Function implementation:

``` bash
  my_example_functions/
  ├── environment.yaml
  ├── mymodule.py
  └── requirements.txt
```


Code for a Function:

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

Environment file to define runtime and Function entrypoints:

``` yaml title="environment.yaml"
runtime: python3.10
version: v1
functions:
  - name: send_doc_to_erp
    entrypoint: mymodule.send_doc_to_erp
```


Define requirements:

``` python title="requirements.txt"
contactsoftware-functions
```

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
