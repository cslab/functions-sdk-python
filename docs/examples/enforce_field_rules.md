Functions can be used to validate user input and ensure that fields on, for example, parts or documents are filled out correctly.


### Required field based on Part category
This example shows how you can enforce that parts in the category *"Single Part"* must have a material assigned.

The example Function can be connected to the [PartCreateCheckEvent](../reference/events.md#partcreatecheckevent) and [PartModifyCheckEvent](../reference/events.md#partmodifycheckevent). It will return an [AbortAndShowErrorAction](../reference/actions.md#abortandshowerroraction) to abort the creation or modification of the part if the condition is not met.

```python
from csfunctions import MetaData, Service
from csfunctions.actions import AbortAndShowErrorAction
from csfunctions.events import (
    PartCreateCheckEvent,
    PartModifyCheckEvent,
)


def single_part_needs_material(
    metadata: MetaData,
    event: PartCreateCheckEvent | PartModifyCheckEvent,
    service: Service,
):
    """
    If a part of category 'Single Part' is created or modified, a material must be assigned.
    This should be checked when the part is created or modified.
    """

    for part in event.data.parts:
        # The event contains a list of parts that are about to be created or modified
        if part.t_kategorie_name_en == "Single Part" and not part.material_object_id:
            return AbortAndShowErrorAction(
                message="A material must be assigned to a part of category 'Single Part'."
            )

```

### Require parts to be classified before release

Classification is a powerful tool for organizing your parts. However, even the best tool is only effective if users actually use it.
With this example Function, you can require that parts are classified before they can be released.

This Function should be connected to the [PartReleaseCheckEvent](../reference/events.md#partreleasecheckevent) and will return an [AbortAndShowErrorAction](../reference/actions.md#abortandshowerroraction) to prevent the release if classification data is missing.

The example code demonstrates how to fetch classification data for parts from the [CIM Database Cloud GraphQL API](https://saas-docs.contact-cloud.com/latest-en/admin/admin-contact_cloud/saas_admin/webhooks_graphql){:target="_blank"}. The Function then checks if any classification data is present, but you can easily expand this to check for specific classes.

```python
from csfunctions import MetaData, Service
from csfunctions.actions import AbortAndShowErrorAction
from csfunctions.events import (
    PartReleaseCheckEvent,
)
import requests


def fetch_part_classification_property_codes(cdb_object_id: str, metadata: MetaData) -> list[str]:
    """
    Returns a list of classification property codes for a given object ID.
    """

    graphql_url = str(metadata.db_service_url).rstrip("/") + "/graphql/v1"
    query = f"""{{
        object_property_values(ref_object_id: "{cdb_object_id}") {{
            property_code
        }}
    }}
    """
    response = requests.post(
        graphql_url,
        headers={"Authorization": f"Bearer {metadata.service_token}"},
        json={"query": query},
    )
    response.raise_for_status()
    data = response.json()
    return [
        item["property_code"]
        for item in data["data"]["object_property_values"]
    ]


def parts_need_classification(
    metadata: MetaData,
    event: PartReleaseCheckEvent,
    service: Service,
):
    """
    Parts must be classified before they can be released.
    """

    for part in event.data.parts:
        # The event contains a list of parts that are about to be released
        # For each part, fetch the classification property codes and check if they are empty
        property_codes = fetch_part_classification_property_codes(part.cdb_object_id, metadata)
        if not property_codes:
            return AbortAndShowErrorAction(
                message=f"The part '{part.eng_benennung or part.benennung}' is missing classification data."
            )

```
