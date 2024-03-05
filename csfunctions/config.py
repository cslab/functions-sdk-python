from pydantic import BaseModel


class FunctionModel(BaseModel):
    name: str
    entrypoint: str


class ConfigModel(BaseModel):
    runtime: str
    version: str
    functions: list[FunctionModel]
