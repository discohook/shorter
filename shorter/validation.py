import os
from urllib.parse import urlparse

from cerberus import TypeDefinition, Validator

from shorter import config
from shorter.errors import BadRequestError


def is_url(field, value, error):
    try:
        parsed = urlparse(value)

        if parsed.scheme not in {"http", "https"}:
            return error(field, "invalid url")
    except (TypeError, ValueError):
        return error(field, "invalid url")


def allowed_host(field, value, error):
    parsed = urlparse(value)

    if config.allowed_hosts and parsed.hostname not in config.allowed_hosts:
        return error(field, "hostname not allowed")


def validate(document, schema):
    validator = Validator(schema)

    if not validator.validate(document, normalize=True):
        raise BadRequestError(
            "Request body does not match validation schema",
            {"errors": validator.errors},
        )

    return validator.normalized(document)


CREATE_SCHEMA = {
    "url": {
        "type": "string",
        "required": True,
        "check_with": (is_url, allowed_host),
    },
    "ttl": {
        "type": "integer",
        "required": False,
        "default": config.max_ttl,
        "min": -1,
        "max": float("inf") if config.max_ttl == -1 else config.max_ttl,
    },
}
