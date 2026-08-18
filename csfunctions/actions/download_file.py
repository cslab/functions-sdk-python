from typing import Literal

from pydantic import Field

from .base import ActionNames, BaseAction


class DownloadFileAction(BaseAction):
    name: Literal[ActionNames.DOWNLOAD_FILE] = ActionNames.DOWNLOAD_FILE
    temp_file_id: str = Field(
        ...,
        description="ID of the temporary file the user should download. "
        "Use service.temp_file.upload() to create a temporary file and get its ID.",
    )
