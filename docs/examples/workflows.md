# Working with workflows

Functions can interact with workflows. You can trigger Functions from within workflows using the [Trigger Webhook](https://saas-docs.contact-cloud.com/latest-en/admin/admin-contact_cloud/saas_admin/webhooks_workflow){:target="_blank"} task, and you can even start new workflows by using the [StartWorkflowAction](../reference/actions.md#startworkflowaction)!


## Start a workflow on EC status change

This example shows how to start a workflow template in response to an engineering change status change.

!!! note
    Starting workflows in response to engineering change status changes is already possible in CIM Database Cloud without the use of Functions. However, Functions allow you to dynamically select different templates and fill out task parameters based on the nature of the change.

This example uses a very simple template containing just an *information task*. If an engineering change contains external parts, users with the *External Part Manager* role should be notified of the planned change during the evaluation phase.

You can easily adapt this example to your use case by adding additional tasks to the template or changing the conditions under which the workflow should be started.

```python
from csfunctions.actions.start_workflow import (
    StartWorkflowAction,
    Subject,
    TaskConfiguration,
)
from csfunctions.events import EngineeringChangeStatusChangedEvent
from csfunctions import MetaData

# Change these to match your template and roles!
TEMPLATE_ID = "PT00000002"
INFORMATION_TASK_ID = "T00000008"
INFORM_ROLE = "External Part Manager"


def start_workflow_on_ec_status_change(
    metadata: MetaData, event: EngineeringChangeStatusChangedEvent, service
):
    if event.data.engineering_change.status != 30:
        # Only start the workflow if the status changed to 30 (Evaluation)
        return

    # Check if the EC contains external parts
    if not any(
        part.t_kategorie_name_en.startswith("External")
        for part in event.data.engineering_change.planned_changes_parts
    ):
        # No external parts, so we don't need to start the workflow
        return

    return StartWorkflowAction(
        template_id=TEMPLATE_ID,
        title=f"Information about EC {event.data.engineering_change.cdb_ec_id}",
        # Attach the engineering change to the workflow
        global_briefcase_object_ids=[
            event.data.engineering_change.cdb_object_id],
        task_configurations=[
            TaskConfiguration(
                task_id=INFORMATION_TASK_ID,
                description="An engineering change containing external parts moved to the evaluation phase.",
                recipients=[
                    Subject(
                        subject_type="Common Role",
                        subject_id=INFORM_ROLE,
                    )
                ],
            )
        ],
    )
```

!!! note
    To successfully execute this example, you need to:

    - Create a workflow template with an information task and adjust the `TEMPLATE_ID` and `INFORMATION_TASK_ID` to match them.
    - Create and assign an "External Part Manager" role to a user.
