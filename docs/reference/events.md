Events always have a `name` and a `data` attribute. The contents of those attributes depend on the type of the event.


## DocumentCreateCheckEvent
`csfunctions.events.DocumentCreateCheckEvent`

This event is fired when a user tries to create or copy a document. Raising an exception will prevent the creation.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**DocumentCreateCheckEvent.name:** document_create_check

**DocumentCreateCheckEvent.data:**

| Attribute | Type                                  | Description                                     |
| --------- | ------------------------------------- | ----------------------------------------------- |
| documents | list[[Document](objects.md#document)] | List of documents that are about to be created. |
| parts     | list[[Part](objects.md#part)]         | List of parts that belong to the documents.     |

## DocumentModifyCheckEvent
`csfunctions.events.DocumentModifyCheckEvent`

This event is fired when a user tries to modify a document. Raising an exception will prevent the modification.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**DocumentModifyCheckEvent.name:** document_modify_check

**DocumentModifyCheckEvent.data:**

| Attribute | Type                                  | Description                                      |
| --------- | ------------------------------------- | ------------------------------------------------ |
| documents | list[[Document](objects.md#document)] | List of documents that are about to be modified. |
| parts     | list[[Part](objects.md#part)]         | List of parts that belong to the documents.      |


## DocumentReleaseCheckEvent
`csfunctions.events.DocumentReleaseCheckEvent`

This event is fired when a user tries to release a document. Raising an exception will prevent the release. If the release is done via the express release, the event is triggered before reviewers are notified.
Be aware that the document is not released yet and the release might still be aborted for other reasons (e.g. the reviewers don't give approval), so don't sent the document to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**DocumentReleaseCheckEvent.name:** document_release_check

**DocumentReleaseCheckEvent.data:**

| Attribute   | Type                                  | Description                                 |
| ----------- | ------------------------------------- | ------------------------------------------- |
| documents   | list[[Document](objects.md#document)] | List of documents that will be released.    |
| parts       | list[[Part](objects.md#part)]         | List of parts that belong to the documents. |
| dialog_data | DocumentReleaseDialogData             | Contents of the dialog.                     |

**DocumentReleaseCheckDialogData:**

| Attribute      | Type        | Description           |
| -------------- | ----------- | --------------------- |
| cdbprot_remark | str \| None | Remark                |
| cdb_ec_id      | str \| None | Engineering Change ID |

## DocumentReleasedEvent
`csfunctions.events.DocumentReleasedEvent`

This event is fired **after** a document has been released. Raising an exception thus can not prevent the release.

**Supported actions:**

- [StartWorkflowAction](actions.md#startworkflowaction)

**DocumentReleasedEvent.name:** document_released

**DocumentReleasedEvent.data:**

| Attribute   | Type                                  | Description                                          |
| ----------- | ------------------------------------- | ---------------------------------------------------- |
| documents   | list[[Document](objects.md#document)] | List of documents that were released.                |
| parts       | list[[Part](objects.md#part)]         | List of parts that belong to the released documents. |
| dialog_data | DocumentReleaseDialogData             | Contents of the dialog.                              |

**DocumentReleasedDialogData:**

| Attribute      | Type        | Description           |
| -------------- | ----------- | --------------------- |
| cdbprot_remark | str \| None | Remark                |
| cdb_ec_id      | str \| None | Engineering Change ID |


## DocumentFieldCalculationEvent
`csfunctions.events.DocumentFieldCalculationEvent`

This event is fired when a document is created, modified, copied or indexed. It is triggered after the field calculations defined in the datasheet editor are performed.

The event expects a DataResponse containing a dictionary of field names and their new values. Fields that are not mentioned in the response are not updated.


**DocumentFieldCalculationEvent.name:** document_field_calculation

**DocumentFieldCalculationEvent.data:**

| Attribute | Type                                         | Description                       |
| --------- | -------------------------------------------- | --------------------------------- |
| document  | [Document](objects.md#document)              | Current state of the document     |
| action    | Literal["create", "modify", "copy", "index"] | Action being performed            |
| parts     | list[[Part](objects.md#part)]                | Parts that belong to the document |



## EngineeringChangeReleaseCheck
`csfunctions.events.EngineeringChangeReleaseCheck`

This event is fired when a user tries to release an engineering change. Raising an exception will prevent the release.
Be aware that the engineering change is not released yet and the release might still be aborted for other reasons, so don't sent the engineering change to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**EngineeringChangeReleaseCheck.name:** engineering_change_check_release

**EngineeringChangeReleaseCheck.data:**

| Attribute           | Type                                                    | Description                                        |
| ------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| engineering_changes | list[[EngineeringChange](objects.md#engineeringchange)] | List of engineering changes that will be released. |
| documents           | list[[Document](objects.md#document)]                   | List of included documents.                        |
| parts               | list[[Part](objects.md#part)]                           | List of included parts.                            |


## EngineeringChangeReleasedEvent
`csfunctions.events.EngineeringChangeReleasedEvent`

This event is fired **after** an engineering change has been released. Raising an exception thus can not prevent the release.

**Supported actions:**

- [StartWorkflowAction](actions.md#startworkflowaction)

**EngineeringChangeReleasedEvent.name:** engineering_change_released

**EngineeringChangeReleasedEvent.data:**

| Attribute           | Type                                                    | Description                                     |
| ------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| engineering_changes | list[[EngineeringChange](objects.md#engineeringchange)] | List of engineering changes that were released. |
| documents           | list[[Document](objects.md#document)]                   | List of included documents.                     |
| parts               | list[[Part](objects.md#part)]                           | List of included parts.                         |

## PartCreateCheckEvent
`csfunctions.events.PartCreateCheckEvent`

This event is fired when a user tries to create or copy a part. Raising an exception will prevent the creation.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**PartCreateCheckEvent.name:** part_create_check

**PartCreateCheckEvent.data:**

| Attribute | Type                                  | Description                                         |
| --------- | ------------------------------------- | --------------------------------------------------- |
| parts     | list[[Part](objects.md#part)]         | List of parts that are about to be created.         |
| documents | list[[Document](objects.md#document)] | List of documents that are referenced by the parts. |

## PartModifyCheckEvent
`csfunctions.events.PartModifyCheckEvent`

This event is fired when a user tries to modify a part. Raising an exception will prevent the modification.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**PartModifyCheckEvent.name:** part_modify_check

**PartModifyCheckEvent.data:**

| Attribute | Type                                  | Description                                         |
| --------- | ------------------------------------- | --------------------------------------------------- |
| parts     | list[[Part](objects.md#part)]         | List of parts that are about to be modified.        |
| documents | list[[Document](objects.md#document)] | List of documents that are referenced by the parts. |

## PartReleaseCheckEvent
`csfunctions.events.PartReleaseCheckEvent`

This event is fired when a user tries to release a part. Raising an exception will prevent the release. If the release is done via the express release, the event is triggered before reviewers are notified.
Be aware that the part is not released yet and the release might still be aborted for other reasons (e.g. the reviewers don't give approval), so don't sent the part to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**PartRPartReleaseCheckEventeleaseEvent.name:** part_release_check

**PartReleaseCheckEvent.data:**

| Attribute   | Type                                  | Description                                          |
| ----------- | ------------------------------------- | ---------------------------------------------------- |
| parts       | list[[Part](objects.md#part)]         | List of parts that will released.                    |
| documents   | list[[Document](objects.md#document)] | List of documents that belong to the released parts. |
| dialog_data | PartReleaseDialogData                 | Contents of the dialog.                              |

**PartReleaseCheckDialogData:**

| Attribute      | Type        | Description           |
| -------------- | ----------- | --------------------- |
| cdbprot_remark | str \| None | Remark                |
| cdb_ec_id      | str \| None | Engineering Change ID |


## PartReleasedEvent
`csfunctions.events.PartReleasedEvent`

This event is fired **after** a part has been released. Raising an exception thus can not prevent the release.

**Supported actions:**

- [StartWorkflowAction](actions.md#startworkflowaction)

**PartReleasedEvent.name:** part_released

**PartReleasedEvent.data:**

| Attribute   | Type                                  | Description                                          |
| ----------- | ------------------------------------- | ---------------------------------------------------- |
| parts       | list[[Part](objects.md#part)]         | List of parts that were released.                    |
| documents   | list[[Document](objects.md#document)] | List of documents that belong to the released parts. |
| dialog_data | PartReleasedDialogData                | Contents of the dialog.                              |

**PartReleasedDialogData:**

| Attribute      | Type        | Description           |
| -------------- | ----------- | --------------------- |
| cdbprot_remark | str \| None | Remark                |
| cdb_ec_id      | str \| None | Engineering Change ID |


## PartFieldCalculationEvent
`csfunctions.events.PartFieldCalculationEvent`

This event is fired when a part is created, modified, copied or indexed. It is triggered after the field calculations defined in the datasheet editor are performed.

The event expects a DataResponse containing a dictionary of field names and their new values. Fields that are not mentioned in the response are not updated.

**PartFieldCalculationEvent.name:** part_field_calculation

**PartFieldCalculationEvent.data:**

| Attribute | Type                                         | Description                               |
| --------- | -------------------------------------------- | ----------------------------------------- |
| part      | [Part](objects.md#part)                      | Current state of the part                 |
| action    | Literal["create", "modify", "copy", "index"] | Action being performed                    |
| documents | list[[Document](objects.md#document)]        | List of documents that belong to the part |


## BOMItemFieldCalculationEvent
`csfunctions.events.BOMItemFieldCalculationEvent`

This event is fired when a BOM item is created, modified, copied or indexed. It is triggered after the field calculations defined in the datasheet editor are performed.

The event expects a DataResponse containing a dictionary of field names and their new values. Fields that are not mentioned in the response are not updated.

**BOMItemFieldCalculationEvent.name:** bom_item_field_calculation

**BOMItemFieldCalculationEvent.data:**

| Attribute | Type                                         | Description                                        |
| --------- | -------------------------------------------- | -------------------------------------------------- |
| bom_item  | [BOMItem](objects.md#bomitem)                | Current state of the BOM item                      |
| action    | Literal["create", "modify", "copy", "index"] | Action being performed                             |
| part      | [Part](objects.md#part)                      | Part of the BOM item                               |
| documents | list[[Document](objects.md#document)]        | List of documents that are referenced by the part. |


## WorkflowTaskTriggerEvent
`csfunctions.events.WorkflowTaskTriggerEvent`

This event is fired by the workflow task "Trigger Webhook".

**WorkflowTaskTriggerEvent.name:** workflow_task_trigger

**WorkflowTaskTriggerEvent.data:**

| Attribute           | Type                                                    | Description                                           |
| ------------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| workflows           | list[[Workflow](objects.md#workflow)]                   | List of workflows in this event.                      |
| parts               | list[[Part](objects.md#part)]                           | List of parts attached to the workflow.               |
| documents           | list[[Document](objects.md#document)]                   | List of documents attached to the workflow.           |
| engineering_changes | list[[EngineeringChange](objects.md#engineeringchange)] | List of engineering changes attached to the workflow. |
| briefcases          | list[[Briefcase](objects.md#briefcase)]                 | List of briefcases attached to the workflow.          |

## EngineeringChangeStatusChanged
`csfunctions.events.EngineeringChangeStatusChanged`

This event is fired **after** an engineering change's status has been modified. Raising an exception cannot prevent the status change.

**EngineeringChangeStatusChanged.name:** engineering_change_status_changed

**EngineeringChangeStatusChanged.data:**

| Attribute          | Type                                              | Description                                          |
| ------------------ | ------------------------------------------------- | ---------------------------------------------------- |
| engineering_change | [EngineeringChange](objects.md#engineeringchange) | The engineering change that had its status modified  |
| prev_status        | str                                               | The previous status of the engineering change        |
| documents          | list[[Document](objects.md#document)]             | List of documents attached to the engineering change |
| parts              | list[[Part](objects.md#part)]                     | List of parts attached to the engineering change     |

## EngineeringChangeStatusChangeCheck
`csfunctions.events.EngineeringChangeStatusChangeCheck`

This event is fired when a user tries to modify an engineering change's status. Raising an exception will prevent the status change.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**EngineeringChangeStatusChangeCheck.name:** engineering_change_status_change_check

**EngineeringChangeStatusChangeCheck.data:**

| Attribute          | Type                                              | Description                                               |
| ------------------ | ------------------------------------------------- | --------------------------------------------------------- |
| engineering_change | [EngineeringChange](objects.md#engineeringchange) | The engineering change that will have its status modified |
| target_status      | int                                               | The status the engineering change will be set to          |
| documents          | list[[Document](objects.md#document)]             | List of documents attached to the engineering change      |
| parts              | list[[Part](objects.md#part)]                     | List of parts attached to the engineering change          |


## CustomOperationDocumentEvent
`csfunctions.events.CustomOperationDocumentEvent`


This event is triggered when a custom operation is called on one or more documents.

**Supported actions:**

- [StartWorkflowAction](actions.md#startworkflowaction)
- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**CustomOperationDocumentEvent.name:** custom_operation_document

**CustomOperationDocumentEvent.data:**

| Attribute | Type                                  | Description                                                |
| --------- | ------------------------------------- | ---------------------------------------------------------- |
| documents | list[[Document](objects.md#document)] | List of documents that the custom operation was called on. |
| parts     | list[[Part](objects.md#part)]         | List of parts that belong to the documents.                |

## CustomOperationPartEvent
`csfunctions.events.CustomOperationPartEvent`


This event is triggered when a custom operation is called on one or more parts.

**Supported actions:**

- [StartWorkflowAction](actions.md#startworkflowaction)
- [AbortAndShowErrorAction](actions.md#abortandshowerroraction)

**CustomOperationPartEvent.name:** custom_operation_part

**CustomOperationPartEvent.data:**

| Attribute | Type                                  | Description                                            |
| --------- | ------------------------------------- | ------------------------------------------------------ |
| parts     | list[[Part](objects.md#part)]         | List of parts that the custom operation was called on. |
| documents | list[[Document](objects.md#document)] | List of documents that belong to the parts.            |
