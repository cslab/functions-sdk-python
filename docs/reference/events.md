Events always have a `name` and a `data` attribute. The contents of those attributes depend on the type of the event.

## DocumentReleaseCheckEvent
`csfunctions.events.DocumentReleaseCheckEvent`

This event is fired when a document is about to be released, but **before** the release has happened. Raising an exception will prevent the release.
At this point it is not guaranteed yet that the document will be released, meaning the document should not be sent to e.g. an ERP system.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**DocumentReleaseCheckEvent.name:** document_release_check

**DocumentReleaseCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|documents| list[[Document](objects.md#document)]|List of documents that will be released.|
|parts| list[[Part](objects.md#part)]|List of parts that belong to the documents.|
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

This event is fired when an engineering change is about to be released, but **before** the release has happened. Raising an exception will prevent the release.
At this point it is not guaranteed yet that the engineering change will be released, meaning the engineering change should not be sent to e.g. an ERP system.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**EngineeringChangeReleaseCheck.name:** engineering_change_check_release

**EngineeringChangeReleaseCheck.data:**

|Attribute|Type|Description|
|-|-|-|
|engineering_changes| list[[EngineeringChange](objects.md#engineeringchange)]|List of engineering changes that will be released.|
|documents| list[[Document](objects.md#document)]|List of included documents.|
|parts| list[[Part](objects.md#part)]|List of included parts.|


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

## PartReleaseCheckEvent
`csfunctions.events.PartReleaseCheckEvent`

This event is fired when a part is about to be released, but **before** the release has happened. Raising an exception will prevent the release.
At this point it is not guaranteed yet that the part will be released, meaning the part should not be sent to e.g. an ERP system.

**Supported actions:**

- [AbortAndShowErrorAction](actions.md#AbortAndShowErrorAction)

**PartRPartReleaseCheckEventeleaseEvent.name:** part_release_check

**PartReleaseCheckEvent.data:**

|Attribute|Type|Description|
|-|-|-|
|parts| list[[Part](objects.md#part)]|List of parts that will released.|
|documents| list[[Document](objects.md#document)]|List of documents that belong to the released parts.|
|dialog_data|PartReleaseDialogData|Contents of the dialog.|

**PartReleaseCheckDialogData:**

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
