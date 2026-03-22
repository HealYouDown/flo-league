import enum
import inspect

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

import src.enums as enums_module


def generate_openapi_id(route: APIRoute) -> str:
    name = route.name
    name = name.replace("_route", "")
    return name


def add_enum_names(schema) -> None:
    # Dynamically adds an x-enumNames field to the OpenAPI spec
    # which allows hey-api to generate named enums in frontend
    enums = {}
    for name, obj in inspect.getmembers(enums_module):
        if inspect.isclass(obj) and issubclass(obj, enum.Enum):
            enums[obj.__name__] = obj

    for name, model in schema["components"]["schemas"].items():
        if "enum" in model and "title" in model:
            enum_cls = enums.get(model["title"])
            if enum_cls and issubclass(enum_cls, enum.Enum):
                model["x-enumNames"] = [e.name for e in enum_cls]


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Florensia PvP League API",
        version="0.1.0",
        routes=app.routes,
    )
    add_enum_names(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema
