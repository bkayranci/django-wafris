import time
from ipaddress import ip_address, IPv4Address, IPv6Address
from redis.connection import ConnectionPool
from redis.client import Redis

from django_wafris.settings import wafris_settings

base = __file__.rsplit("/", 1)[0]


class WafrisCore(Redis):

    @classmethod
    def from_url(cls, url, **kwargs):
        single_connection_client = kwargs.pop("single_connection_client", False)
        connection_pool = ConnectionPool.from_url(url, **kwargs)
        client = cls(
            connection_pool=connection_pool,
            single_connection_client=single_connection_client,
        )
        client.auto_close_connection_pool = True
        cls.instance = client
        return client

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__lua_script_path = f"{base}/lua/wafris_core.lua"
        self.hash = None

        with open(self.__lua_script_path, "r") as f:
            self.hash = self.script_load(f.read())
            self.hset(
                "waf-settings", mapping={"version": "v0.0.1", "client": "django-wafris"}
            )


def request_ip_to_numeric_string(req, logger):
    req.remote_addr = req.META.get("REMOTE_ADDR", None)
    if req.remote_addr is None:
        logger.error("[Wafris] Request IP is null")
        return ""

    try:
        ip_obj = ip_address(req.remote_addr)

        if isinstance(ip_obj, IPv4Address) or isinstance(ip_obj, IPv6Address):
            return str(int(ip_obj))
    except ValueError as e:
        logger.error(f"[Wafris] Error parsing IP address {req.remote_addr}: {str(e)}")
    except Exception as e:
        logger.error(
            f"[Wafris] Unexpected error {e.__class__.__name__} parsing IP address {req.remote_addr}: {str(e)}"
        )

    return ""


def request_to_redis_arguments(request, logger):

    map_data = {
        "ip": request.META["REMOTE_ADDR"],
        "decimalIp": request_ip_to_numeric_string(request, logger),
        "time": int(time.time() * 1000),
        "userAgent": request.META["HTTP_USER_AGENT"],
        "path": request.META["PATH_INFO"],
        "query": request.META["QUERY_STRING"],
        "host": request.META["HTTP_HOST"],
        "method": request.META["REQUEST_METHOD"],
    }

    return map_data


wafris = WafrisCore.from_url(wafris_settings.get("REDIS_URL"))
