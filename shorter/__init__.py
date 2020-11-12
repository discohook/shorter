import asyncio
import os

import aioredis
from quart import Quart, exceptions

import shorter.bp.shortener
from shorter.errors import ApiError

app = Quart(__name__)

app.register_blueprint(shorter.bp.shortener.bp)


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()

    app.redis = await aioredis.create_redis_pool(
        os.environ.get("REDIS_ADDRESS"),
        loop=loop,
        encoding="utf-8",
    )


@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    return {
        "message": error.message,
        **error.payload,
    }, error.status_code


@app.errorhandler(exceptions.HTTPException)
def handle_exception(exception: exceptions.HTTPException):
    try:
        return {"message": exception.name}, exception.status_code
    except AttributeError:
        return {"message": "Internal Server Error"}, 500
