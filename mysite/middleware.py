import time

from django.http import HttpRequest, HttpResponse

from posts.decorators import queries_stat


class StatsMiddleware:
    """Timestamps the entire request
    """
    def __init__(self, get_response):
        self.get_response = queries_stat(get_response)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        # Add the header. Or do other things, my use case is to send a monitoring metric
        print(f'Request {request.path} time {duration}\n')
        return response
