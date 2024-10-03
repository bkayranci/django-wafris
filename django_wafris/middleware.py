import logging

from django.http import HttpResponse
from django_wafris.wafris_core import request_to_redis_arguments, wafris

logger = logging.getLogger(__name__)


class WafrisMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        data = request_to_redis_arguments(
            request,
            logger,
        )

        r = wafris.evalsha(
            wafris.hash,
            len(data.keys()),
            *[*data.keys(), *data.values()],
        )
        if r.decode() == "Blocked":
            return HttpResponse("Blocked", status=403)
        response = self.get_response(request)
        return response

    def process_response(self, request, response):

        if response.status_code == 200:
            response.content = response.content.replace(b"WAFRIS", b"WAFRIS v1.0")
        return response
