import os

import dotenv

dotenv.load_dotenv()


redis_address = os.environ.get("REDIS_ADDRESS")

allowed_hosts = os.environ.get("SHORTEN_ALLOWED_HOSTS", "*").split(",")
if allowed_hosts == ["*"]:
    allowed_hosts = None
else:
    allowed_hosts = set(allowed_hosts)

max_ttl = int(os.environ.get("SHORTEN_MAX_TTL", "-1"))
