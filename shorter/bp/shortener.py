from datetime import datetime, timedelta

from quart import Blueprint, current_app, redirect, request, url_for
from shorter import config
from shorter.common import generate_shortname
from shorter.errors import NotFoundError
from shorter.validation import CREATE_SCHEMA, validate

bp = Blueprint("shortener", __name__)


@bp.route("/create", methods=["POST"])
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
    await current_app.redis.set(shortname, url)
    await current_app.redis.expire(shortname, ttl)

    url = request.url_root.strip("/") + url_for("shortener.go", shortname=shortname)

    return {
        "id": shortname,
        "url": url,
        "expires": expires,
    }


@bp.route("/go/<shortname>")
async def go(shortname):
    url = await current_app.redis.get(shortname)

    if not url:
        raise NotFoundError(f"Shorten {shortname!r} not found")

    return redirect(url)
