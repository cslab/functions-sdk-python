from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, Field


class MetaData(BaseModel):
    def __init__(
        self,
        app_lang: str,
        app_user: str,
        request_id: str,
        request_datetime: datetime,
        transaction_id: str,
        instance_url: str,
        db_service_url: str | None = None,
        **kwargs
    ):
        super().__init__(
            app_lang=app_lang,
            app_user=app_user,
            request_id=request_id,
            db_service_url=db_service_url,
            request_datetime=request_datetime,
            transaction_id=transaction_id,
            instance_url=instance_url,
            **kwargs
        )

    app_lang: str = Field(..., description="ISO code of the session language that triggered the webhook.")
    app_user: str = Field(..., description="User id of the user that triggered the webhook. (personalnummer)")
    request_id: str = Field(..., description="Unique identifier of this request.")
    service_url: AnyHttpUrl | None = Field(None, description="Url of the access service. None if not available.")
    service_token: str | None = Field(None, description="Token for the access service. None if not available.")
    request_datetime: datetime = Field(..., description="Time when the request was started.")
    transaction_id: str = Field(..., description="Unique identifier of the transaction.")
    instance_url: AnyHttpUrl = Field(..., description="URL to the instance where the webhook was triggered.")
    db_service_url: AnyHttpUrl | None = Field(
        None, description="URL to the DB Access Service responsible for the instance."
    )
