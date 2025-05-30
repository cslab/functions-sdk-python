# Field calculation

The datasheet editor in CIM Database Cloud already allows you to define some basic [field calculations](https://saas-docs.contact-cloud.com/2025.13.1-en/admin/admin-contact_cloud/saas_admin/app_setup_data_edit_field_calc){:target="_blank"} to fill out fields automatically.

However, the Python expressions available in the datasheet editor are limited. Functions allow for much more flexibility in defining your field calculations, enabling you to do things like *fetching external data* or *referencing other objects*.

Field calculations with Functions utilize the `<Object>FieldCalculationEvent`, e.g. [PartFieldCalculationEvent](../reference/events.md#partfieldcalculationevent), which expects the response to contain a `DataResponse` with a dictionary of the fields that should be updated.

```python
return DataResponse(data={"somefield": "new value"})
```


## Custom part number for external parts

This example shows you the basics of calculating fields with Functions and how to use the `service` parameter to generate a new number.

The example Function checks if the part is an *"External"* part and generates a custom part number for it.

```python
from csfunctions import DataResponse
from csfunctions.events import PartFieldCalculationEvent
from csfunctions.metadata import MetaData
from csfunctions.service import Service

def calculate_part_number(metadata: MetaData, event: PartFieldCalculationEvent, service: Service):
    """
    Example Function.
    This function is triggered when a part field should be calculated.
    For "External" parts, we want to set the part number as "E-000123".
    All other parts should keep the standard part number.
    """
    if event.data.action != "create":
        # Part number can only be set when the part is created
        return

    # Match "External Single Part" or "External Assembly"
    if event.data.part.t_kategorie_name_en.startswith("External"):
        # Generate a new number using the service
        new_number = service.generator.get_number("external_part_number")
        # new_number is an integer, so we need to convert it to a string
        # and pad it with leading zeros to 6 digits
        new_part_number = str(new_number).zfill(6)
        # Add the prefix "E-" to the number
        new_part_number = "E-" + new_part_number
        # Return the new part number (teilenummer)
        return DataResponse(data={"teilenummer": new_part_number})
```

!!! tip
    You can check `event.data.action` to decide for which operations (*copy*, *create*, *index*, and *modify*) you want your field calculation to return a new value.
    Some fields, like part number (*teilenummer*), can only be set during the initial creation.

## Translate a part name with DeepL

This example uses the [DeepL API](https://www.deepl.com){:target="_blank"} to translate the part name of newly created parts from German to English or vice versa, depending on which name is already provided. You can easily adapt this example to translate other fields or use a different translation API if needed.

```python
import os
from csfunctions import DataResponse
from csfunctions.events import PartFieldCalculationEvent
import requests

# Set the DEEPL_API_KEY during deployment like this:
# cfc env deploy <environment name> --environment-variables "DEEPL_API_KEY=<your API key>"
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def part_field_calculation(metadata, event: PartFieldCalculationEvent, service):
    if event.data.action != "create":
        # Only translate on creation
        return

    if event.data.part.eng_benennung and not event.data.part.benennung:
        # English part name is set but German name is missing
        # -> translate English name to German
        translated_text = translate_text(
            event.data.part.eng_benennung, target_lang="DE", source_lang="EN")
        return DataResponse(data={"benennung": translated_text})
    elif event.data.part.benennung and not event.data.part.eng_benennung:
        # German name is set but English name is missing
        # -> translate German name to English
        translated_text = translate_text(
            event.data.part.benennung, target_lang="EN", source_lang="DE")
        return DataResponse(data={"eng_benennung": translated_text})

def translate_text(text, target_lang, source_lang=None):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang.upper()
    }
    if source_lang:
        data["source_lang"] = source_lang.upper()

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]

```

!!! note
    This example requires a DeepL API key to function. Adding secrets like API keys to your code is a bad practice, which is why the example fetches the API key from an environment variable.

    You can set environment variables during deployment of your Function to the CIM Database Cloud Functions infrastructure like this:

    `cfc env deploy <environment name> --environment-variables "DEEPL_API_KEY=<your API key>"`
