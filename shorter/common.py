import secrets
import string

from quart import current_app

ALPHABET = string.digits + string.ascii_lowercase


async def generate_shortname(length: int):
    for _ in range(16):
        possible_shortname = "".join(secrets.choice(ALPHABET) for _ in range(length))

        if not await current_app.redis.exists(possible_shortname):
            return possible_shortname

    return generate_shortname(length + 1)
