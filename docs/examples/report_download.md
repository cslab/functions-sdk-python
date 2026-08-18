# Report Download

This example shows how you can use a custom operation to generate a report for the
selected documents and have the users browser download it right away, without attaching
the report to a business object.

The report is built in memory and handed to the user with
[`service.temp_file.upload()`](../reference/service.md#upload-a-file-for-download) and a
[DownloadFileAction](../reference/actions.md#downloadfileaction).

The example uses [python-docx](https://python-docx.readthedocs.io/en/latest/) to generate a Word file.
To install the library in your Function, you need to add it to the `requirements.txt`:

```requirements.txt
contactsoftware-functions
python-docx
```

```python
import io
from datetime import datetime

from docx import Document as DocxDocument

from csfunctions import MetaData, Service
from csfunctions.actions import DownloadFileAction
from csfunctions.events import CustomOperationDocumentEvent
from csfunctions.objects import Document


def report_download(metadata: MetaData, event: CustomOperationDocumentEvent, service: Service):
    """
    Generates one report for all documents the custom operation was called on and
    lets the user download it directly in the browser.
    """

    report = _create_report(event.data.documents)

    # python-docx can save into a stream, so we never have to touch the file system
    stream = io.BytesIO()
    report.save(stream)
    stream.seek(0)

    file_name = f"report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.docx"

    # upload the report as a temporary file, the user may download it once
    temp_file_id = service.temp_file.upload(
        stream=stream,
        filename=file_name,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # tell CIM Database Cloud to make the browser download the file
    return DownloadFileAction(temp_file_id=temp_file_id)


def _create_report(documents: list[Document]) -> DocxDocument:
    """Creates a simple Word report for the given documents."""
    doc = DocxDocument()

    doc.add_heading("Document Report", 0)
    doc.add_paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc.add_paragraph(f"Documents in this report: {len(documents)}")

    for document in documents:
        doc.add_heading(f"{document.z_nummer}@{document.z_index}", level=1)
        doc.add_paragraph(f"Title: {document.titel}")
        doc.add_paragraph(f"Created On: {document.cdb_cdate}")
        doc.add_paragraph(f"Created By: {document.cdb_cpersno}")

    return doc

```

!!! warning
    The user is blocked while the Function runs, and a Function may only run for about
    30 seconds. That is plenty for a report over the selected documents, but it is not
    enough to collect and zip a large set of CAD files.

    Note also that only **one** file can be downloaded per operation. If your Function
    produces several files, pack them into a ZIP archive.
