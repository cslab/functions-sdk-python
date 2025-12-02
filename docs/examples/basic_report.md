# Basic Report

This example shows how you can use custom operations to generate a basic report on a document and attach that report to the document.

The example uses [python-docx](https://python-docx.readthedocs.io/en/latest/) to generate a Word file.
To install the library in your Function, you need to add it to the `requirements.txt`:

```requirements.txt
contactsoftware-functions
python-docx
```

```python
import os
import tempfile
from datetime import datetime

import requests
from docx import Document as DocxDocument

from csfunctions import MetaData, Service
from csfunctions.events import CustomOperationDocumentEvent
from csfunctions.objects import Document


def simple_report(metadata: MetaData, event: CustomOperationDocumentEvent, service: Service):
    """
    Generates a simple report for each document the custom operation is called on.
    The report contains basic information about the document and is saved as a new file
    named "myreport.docx" within the document.
    """

    for document in event.data.documents:
        # generate a report for each document
        report = _create_report(document, metadata)

        temp_file_path = None
        try:
            # we need to use a tempfile, because the rest of the filesystem is read-only
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                temp_file_path = tmp.name
            report.save(temp_file_path)

            # check if the document already has a report file, so we can overwrite it
            file_name = "myreport.docx"
            existing_file = next((file for file in document.files if file.cdbf_name == file_name), None)

            with open(temp_file_path, "rb") as file_stream:
                if existing_file:
                    # overwrite the existing report file
                    # we set check_access to false to allow attaching reports to released documents
                    service.file_upload.upload_file_content(
                        file_object_id=existing_file.cdb_object_id, stream=file_stream, check_access=False
                    )
                else:
                    # create a new one
                    # we set check_access to false to allow attaching reports to released documents
                    service.file_upload.upload_new_file(
                        parent_object_id=document.cdb_object_id,  # type: ignore
                        filename=file_name,
                        stream=file_stream,
                        check_access=False,
                    )
        finally:
            if temp_file_path:
                # Clean up temp file
                os.unlink(temp_file_path)


def _fetch_person_name(persno: str, metadata: MetaData) -> str | None:
    """Fetches the name of a person given their personnel number via GraphQL."""
    graphql_url = str(metadata.db_service_url).rstrip("/") + "/graphql/v1"
    headers = {"Authorization": f"Bearer {metadata.service_token}"}

    query = f"""
      {{
        persons(personalnummer: \"{persno}\", max_rows: 1) {{
        name
        }}
       }}
    """
    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": query},
    )
    response.raise_for_status()
    data = response.json()
    persons = data["data"]["persons"]
    if persons:
        return persons[0]["name"]
    return None


def _create_report(document: Document, metadata: MetaData) -> DocxDocument:
    """Creates a simple Word report for the given document."""
    doc = DocxDocument()

    doc.add_heading("Simple Report", 0)

    report_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc.add_paragraph(f"Report generated on: {report_time_string}")

    # add some basic information about the document
    doc.add_heading("Document Information", level=1)
    doc.add_paragraph(f"Document ID: {document.z_nummer}@{document.z_index}")
    doc.add_paragraph(f"Title: {document.titel}")
    doc.add_paragraph(f"Created On: {document.cdb_cdate}")

    # Fetch the name of the person who created the document via GraphQL
    person_name = _fetch_person_name(document.cdb_cpersno, metadata)
    doc.add_paragraph(f"Created By: {person_name or document.cdb_cpersno}")

    return doc

```
