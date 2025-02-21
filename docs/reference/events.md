Events always have a `name` and a `data` attribute. The contents of those attributes depend on the type of the event.


## DocumentCreateCheckEvent
`csfunctions.events.DocumentCreateCheckEvent`

This event is fired when a user tries to create or copy a document. Raising an exception will prevent the creation.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**DocumentCreateCheckEvent.name:** document_create_check

**DocumentCreateCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|documents| list[[Document](objects.md#document)]|List of documents that are about to be created.|
|attached_parts| list[[Part](objects.md#part)]|List of parts that belong to the documents.|
|attached_documents| list[[Document](objects.md#document)]|Contains the original document(s) if a document is a copy.|

## DocumentModifyCheckEvent
`csfunctions.events.DocumentModifyCheckEvent`

This event is fired when a user tries to modify a document. Raising an exception will prevent the modification.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**DocumentModifyCheckEvent.name:** document_modify_check

**DocumentModifyCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|documents| list[[Document](objects.md#document)]|List of documents that are about to be modified.|
|attached_parts| list[[Part](objects.md#part)]|List of parts that belong to the documents.|


## DocumentReleaseCheckEvent
`csfunctions.events.DocumentReleaseCheckEvent`

This event is fired when a user tries to release a document. Raising an exception will prevent the release. If the release is done via the express release, the event is triggered before reviewers are notified.
Be aware that the document is not released yet and the release might still be aborted for other reasons (e.g. the reviewers don't give approval), so don't sent the document to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**DocumentReleaseCheckEvent.name:** document_release_check

**DocumentReleaseCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|documents| list[[Document](objects.md#document)]|List of documents that will be released.|
|attached_parts| list[[Part](objects.md#part)]|List of parts that belong to the documents.|
|dialog_data|DocumentReleaseDialogData|Contents of the dialog.|

**DocumentReleaseCheckDialogData:**

|Attribute|Type|Description|
|-|-|-|
|cdbprot_remark|str \| None | Remark|
|cdb_ec_id|str \| None| Engineering Change ID|

## DocumentReleaseEvent
`csfunctions.events.DocumentReleaseEvent`

This event is fired **after** a document has been released. Raising an exception thus can not prevent the release.

**DocumentReleaseEvent.name:** document_release

**DocumentReleaseEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|documents| list[[Document](objects.md#document)]|List of documents that were released.|
|parts| list[[Part](objects.md#part)]|List of parts that belong to the released documents.|
|dialog_data|DocumentReleaseDialogData|Contents of the dialog.|

**DocumentReleaseDialogData:**

|Attribute|Type|Description|
|-|-|-|
|cdbprot_remark|str \| None | Remark|
|cdb_ec_id|str \| None| Engineering Change ID|


## EngineeringChangeReleaseCheck
`csfunctions.events.EngineeringChangeReleaseCheck`

This event is fired when a user tries to release an engineering change. Raising an exception will prevent the release.
Be aware that the engineering change is not released yet and the release might still be aborted for other reasons, so don't sent the engineering change to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**EngineeringChangeReleaseCheck.name:** engineering_change_check_release

**EngineeringChangeReleaseCheck.data:**

|Attribute|Type|Description|
|-|-|-|
|engineering_changes| list[[EngineeringChange](objects.md#engineeringchange)]|List of engineering changes that will be released.|
|attached_documents| list[[Document](objects.md#document)]|List of included documents.|
|attached_parts| list[[Part](objects.md#part)]|List of included parts.|


## EngineeringChangeRelease
`csfunctions.events.EngineeringChangeRelease`

This event is fired **after** an engineering change has been released. Raising an exception thus can not prevent the release.

**EngineeringChangeRelease.name:** engineering_change_release

**EngineeringChangeRelease.data:**

|Attribute|Type|Description|
|-|-|-|
|engineering_changes| list[[EngineeringChange](objects.md#engineeringchange)]|List of engineering changes that were released.|
|documents| list[[Document](objects.md#document)]|List of included documents.|
|parts| list[[Part](objects.md#part)]|List of included parts.|

## PartCreateCheckEvent
`csfunctions.events.PartCreateCheckEvent`

This event is fired when a user tries to create or copy a part. Raising an exception will prevent the creation.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**PartCreateCheckEvent.name:** part_create_check

**PartCreateCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|parts| list[[Part](objects.md#part)]|List of parts that are about to be created.|
|attached_parts| list[[Part](objects.md#part)]|Contains the original part(s) if a part is a copy.|

## PartModifyCheckEvent
`csfunctions.events.PartModifyCheckEvent`

This event is fired when a user tries to modify a part. Raising an exception will prevent the modification.
The event is triggered before any field calculations are performed.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**PartModifyCheckEvent.name:** part_modify_check

**PartModifyCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|parts| list[[Part](objects.md#part)]|List of parts that are about to be modified.|

## PartReleaseCheckEvent
`csfunctions.events.PartReleaseCheckEvent`

This event is fired when a user tries to release a part. Raising an exception will prevent the release. If the release is done via the express release, the event is triggered before reviewers are notified.
Be aware that the part is not released yet and the release might still be aborted for other reasons (e.g. the reviewers don't give approval), so don't sent the part to e.g. an ERP system yet.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**PartRPartReleaseCheckEventeleaseEvent.name:** part_release_check

**PartReleaseCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|parts| list[[Part](objects.md#part)]|List of parts that will released.|
|attached_documents| list[[Document](objects.md#document)]|List of documents that belong to the released parts.|
|dialog_data|PartReleaseDialogData|Contents of the dialog.|

**PartReleaseCheckDialogData:**

|Attribute|Type|Description|
|-|-|-|
|cdbprot_remark|str \| None | Remark|
|cdb_ec_id|str \| None| Engineering Change ID|


## PartReleaseEvent
`csfunctions.events.PartReleaseEvent`

This event is fired **after** a part has been released. Raising an exception thus can not prevent the release.

**PartReleaseEvent.name:** part_release

**PartReleaseEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|parts| list[[Part](objects.md#part)]|List of parts that were released.|
|documents| list[[Document](objects.md#document)]|List of documents that belong to the released parts.|
|dialog_data|PartReleaseDialogData|Contents of the dialog.|

**PartReleaseDialogData:**

|Attribute|Type|Description|
|-|-|-|
|cdbprot_remark|str \| None | Remark|
|cdb_ec_id|str \| None| Engineering Change ID|


## WorkflowTaskTriggerEvent
`csfunctions.events.WorkflowTaskTriggerEvent`

This event is fired by the workflow task "Trigger Webhook".

**WorkflowTaskTriggerEvent.name:** workflow_task_trigger

**WorkflowTaskTriggerEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|workflows| list[[Workflow](objects.md#workflow)]|List of workflows in this event.|
|parts| list[[Part](objects.md#part)]|List of parts attached to the workflow.|
|documents| list[[Document](objects.md#document)]|List of documents attached to the workflow.|
|engineering_changes| list[[EngineeringChange](objects.md#engineeringchange)]|List of engineering changes attached to the workflow.|
|briefcases| list[[Briefcase](objects.md#briefcase)]|List of briefcases attached to the workflow.|
