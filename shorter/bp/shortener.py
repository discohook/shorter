from datetime import datetime, timedelta
from urllib.parse import urlunparse

from quart import Blueprint, current_app, redirect, request, url_for
from quart_rate_limiter import rate_limit
from shorter import config
from shorter.common import generate_shortname
from shorter.errors import NotFoundError
from shorter.validation import CREATE_SCHEMA, validate

bp = Blueprint("shortener", __name__)


@bp.route("/create", methods=["POST"])
@rate_limit(limit=60, period=timedelta(minutes=10))
async def create():
    payload = validate(await request.get_json(), CREATE_SCHEMA)

    url = payload["url"]
    ttl = payload["ttl"]
    if ttl == -1:
        ttl = config.max_ttl

    expires = (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
    if ttl == -1:
        expires = None

    shortname = await generate_shortname(8)
    key = f"{current_app.import_name}-shorten-{shortname}"
    await current_app.redis.set(key, url)
    await current_app.redis.expire(key, ttl)

    url = urlunparse(
        (
            request.headers.get("X-Forwarded-Proto", "http"),
            request.headers["Host"],
            url_for("shortener.go", shortname=shortname),
            None,
            None,
            None,
        )
    )

    return {
        "id": shortname,
        "url": url,
        "expires": expires,
    }


@bp.route("/go/<shortname>")
@rate_limit(limit=120, period=timedelta(minutes=10))
async def go(shortname):
    key = f"{current_app.import_name}-shorten-{shortname}"
    url = await current_app.redis.get(key)

    if not url:
        raise NotFoundError(f"Shorten {shortname!r} not found")

    return redirect(url)
