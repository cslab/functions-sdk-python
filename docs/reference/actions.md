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
