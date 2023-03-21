import uuid
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timedelta
from decouple import config


class SessionMiddleware(MiddlewareMixin):
    id = None
    page_size = None

    def process_request(self, request):
        self.id = request.COOKIES.get('id')
        if self.id is None or self.id == 'None':
            self.id = uuid.uuid4().__str__().replace('-', '').lower()

        if self.page_size is None:
            self.page_size = config('PAGE_SIZE')

        return None

    def process_response(self, request, response):
        response.set_cookie('last_visit', str(datetime.now()))
        response.set_cookie('id',
                            str(self.id),
                            path='/',
                            expires=datetime.now() + timedelta(days=365))
        response.set_cookie('page_size', self.page_size)
        return response
