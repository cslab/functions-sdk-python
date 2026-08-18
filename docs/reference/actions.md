Functions can return a list of "Actions" that should be performed in CIM Database Cloud.

```python
from csfunctions.actions import AbortAndShowErrorAction

def my_function(metadata, event, service):
    # this will show an error message to the user
    return AbortAndShowErrorAction(message="Custom error message.")
```

Not all Events support the same actions, so check the supported actions in the [Events documentation](events.md). For example Events that are triggered **after** the release of an object don't support AbortAndShowError, because the release can't be aborted anymore, however the "release check" events do support it.


## AbortAndShowErrorAction

`csfunctions.actions.AbortAndShowErrorAction`

Aborts the current operation and shows an error message to the user.

**Attributes:**

| Attribute | Type | Description                                  |
| --------- | ---- | -------------------------------------------- |
| message   | str  | Error message that will be shown to the user |

## DownloadFileAction

`csfunctions.actions.DownloadFileAction`

Makes the users browser download a file that the Function generated. Upload the file with
[`service.temp_file.upload()`](service.md#upload-a-file-for-download) first and pass the
temporary file ID it returns to this action.

**Attributes:**

| Attribute    | Type | Description                                                                        |
| ------------ | ---- | ---------------------------------------------------------------------------------- |
| temp_file_id | str  | ID of the temporary file, as returned by `service.temp_file.upload()`               |

**Example:**

```python
import io

from csfunctions.actions import DownloadFileAction

def my_function(metadata, event, service):
    temp_file_id = service.temp_file.upload(
        stream=io.BytesIO(b"part_number;name\n123;My Part\n"),
        filename="parts.csv",
    )
    return DownloadFileAction(temp_file_id=temp_file_id)
```

!!! warning
    A few restrictions apply:

    - Only the custom operation events support this action, because the download has to
      be triggered while the user is waiting for the operation to finish.
    - A response can contain **at most one** DownloadFileAction, because the browser can
      only be sent to one URL. Pack multiple files into an archive if you need to.
    - It cannot be combined with an
      [AbortAndShowErrorAction](#abortandshowerroraction) - aborting the operation
      discards the download.
    - The file can be downloaded exactly once, and only by the user the temporary file
      belongs to.

## StartWorkflowAction

`csfunctions.actions.StartWorkflowAction`

Creates a new workflow from a template and starts it.



**Attributes:**

| Attribute                   | Type                    | Description                                                   |
| --------------------------- | ----------------------- | ------------------------------------------------------------- |
| template_id                 | str                     | ID of the workflow template                                   |
| cdb_project_id              | str \| None             | ID of the project in which the workflow should be started     |
| title                       | str                     | Title that the new workflow should have (max. 255 characters) |
| attachment_ids              | list[str]               | List of cdb_object_ids to attach to the workflow              |
| global_briefcase_object_ids | list[str]               | List of cdb_object_ids to attach to the global briefcase      |
| task_configurations         | list[TaskConfiguration] | List of task configurations                                   |

**TaskConfiguration:**

| Attribute   | Type              | Description                                                                                        |
| ----------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| task_id     | str               | Identifier for the task                                                                            |
| responsible | [Subject] \| None | Responsible Subject for the task                                                                   |
| recipients  | list[[Subject]]   | List of recipients  (only used by information tasks)                                               |
| description | str \| None       | Description of the task. If not set, the existing description will be kept. (max. 1024 characters) |
| title       | str \| None       | Title of the task. If not set, the existing title will be kept. (max. 60 characters)               |

**Subject:**

| Attribute    | Type | Description                                                       |
| ------------ | ---- | ----------------------------------------------------------------- |
| subject_id   | str  | ID of the subject, e.g. a role name or "personalnummer"           |
| subject_type | str  | Type of the subject. Can be "Person", "PCS Role" or "Common Role" |
