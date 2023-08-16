import logging

logger = logging.getLogger(__name__)

class ClientLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log only for login URL
        client_ip = None
        user_agent = None

        try:
            client_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')
        except Exception as e:
            logger.error(f'Error in ClientLoggingMiddleware.__call__: {e}')

        response = self.get_response(request)
        if client_ip is None:
            response.set_cookie('client_ip', '')
        else:
            response.set_cookie('client_ip', client_ip)

        if user_agent is None:
            response.set_cookie('user_agent', '')
        else:
            response.set_cookie('user_agent', user_agent)
        return response
