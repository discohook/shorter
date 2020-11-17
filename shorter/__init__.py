import asyncio
import os

import aioredis
from quart import Quart, exceptions
from quart_cors import cors

import shorter.bp.shortener
from shorter import config
from shorter.errors import ApiError
from shorter.ratelimit import rate_limiter

app = Quart(__name__)
app = cors(app)

rate_limiter.init_app(app)


app.register_blueprint(shorter.bp.shortener.bp)


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()

    app.redis = await aioredis.create_redis_pool(
        config.redis_address,
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
