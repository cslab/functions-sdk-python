# Functions Access Service

The Functions Access Service provides access to backend services like number generators and file uploads. These services are available through the `service` parameter that is passed to all Functions.

The Access Service is ratelimited to `100 req/min` per token. Functions receive a fresh token for every call.

```python
from csfunctions import Service

def my_function(metadata, event, service: Service):
    ...

```

## Number Generation


You can use the `service.generator` to generate unique numbers, for example for part numbers or document IDs.

### Methods

- `get_number(name: str) -> int`
    Retrieve one number from the given generator.
- `get_numbers(name: str, count: int) -> list[int]`
    Retrieve multiple numbers from the given generator in one request.
    Maximum for `count` is 100.

**Example:**

```python
new_number = service.generator.get_number("external_part_number")
# Returns an integer, e.g. 123
```

To generate multiple numbers at once:

```python
numbers = service.generator.get_numbers("external_part_number", count=5)
# Returns a list of integers
```

## File Uploads



The `service.file_upload` object allows you to upload new files to the CIM Database Cloud or overwrite existing ones.



### Upload a new file

```python
service.file_upload.upload_new_file(
        self,
        parent_object_id: str,
        filename: str,
        stream: BinaryIO,
        persno: str | None = None,
        check_access: bool = True,
        filesize: int | None = None,
    ) -> str:
```
Creates a new file attached to the parent object and uploads content from the provided stream. Returns the new file object ID.

| Parameter          | Type          | Description                                                                                   |
| ------------------ | ------------- | --------------------------------------------------------------------------------------------- |
| `parent_object_id` | `str`         | The ID of the parent object to which the new file will be attached.                           |
| `filename`         | `str`         | The name of the new file to be uploaded.                                                      |
| `stream`           | `BinaryIO`    | A binary stream containing the file data to upload.                                           |
| `persno`           | `str \| None` | The user/person number uploading the file (defaults to the user that triggered the Function). |
| `check_access`     | `bool`        | Whether to check access permissions before uploading. Defaults to `True`.                     |
| `filesize`         | `int \| None` | Size of the file in bytes (required only if the stream is not seekable).                      |

**Exceptions:**

- `csfunctions.service.Unauthorized`: If th service token is invalid.
- `csfunctions.service.Forbidden`: If access check fails.
- `csfunctions.service.NotFound`: If the parent object does not exist.


!!! info
    Uploading new files performs 3 requests to the Functions Access Service, which count towards the ratelimit of `100 req/min` per token.

**Example:**

```python
with open("myfile.pdf", "rb") as f:
        file_object_id = service.file_upload.upload_new_file(
                parent_object_id="123456",
                filename="myfile.pdf",
                stream=f
        )
```

### Overwrite an existing file

```python
service.file_upload.upload_file_content(
    file_object_id: str,
    stream: BinaryIO,
    persno: str | None = None,
    check_access: bool = True,
    filesize: int | None = None,
    delete_derived_files: bool = True,
    ) -> None
```
Uploads new content to an existing file object, overwriting its previous contents.

| Parameter              | Type          | Description                                                                                                          |
| ---------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `file_object_id`       | `str`         | The ID of the file object to upload to (must already exist).                                                         |
| `stream`               | `BinaryIO`    | A binary stream containing the file data to upload.                                                                  |
| `persno`               | `str \| None` | The user/person number uploading the file (defaults to the user that triggered the Function).                        |
| `check_access`         | `bool`        | Whether to check access permissions before uploading. Defaults to `True`.                                            |
| `filesize`             | `int \| None` | Size of the file in bytes (required only if the stream is not seekable).                                             |
| `delete_derived_files` | `bool`        | Whether to delete derived files (e.g. converted pdfs) after upload and trigger a new conversion. Defaults to `True`. |

!!! warning
    Overwriting files is only possible if the file is not locked!

**Exceptions:**

- `csfunctions.service.Unauthorized`: If th service token is invalid.
- `csfunctions.service.Forbidden`: If access check fails.
- `csfunctions.service.Conflict`: If the file is already locked.
- `csfunctions.service.NotFound`: If the file object does not exist.
- `csfunctions.service.RateLimitExceeded`: If the services rate limit is exceeded.

!!! info
    Uploading new files performs 2 requests to the Functions Access Service, which count towards the ratelimit of `100 req/min` per token.

**Example:**

```python
file = doc.files[0]
with open("updated_file.pdf", "rb") as f:
    service.file_upload.upload_file_content(
        file_object_id=file.cdb_object_id,
        stream=f
    )
```
