import uuid
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timedelta
from decouple import config
import os


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


class Logger:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rem_addr = request.META.get('REMOTE_ADDR')
        user = request.user

        referer = request.META.get('HTTP_REFERER')
        if referer is None:
            referer = request.META.get('PATH_INFO')

        querystring = request.META.get("QUERY_STRING")
        if querystring is None:
            querystring = ''
        else:
            querystring = '?' + querystring
        url = referer + querystring

        user_agent = request.META.get('HTTP_USER_AGENT')

        log_txt = f'{self.timestamp()};{rem_addr};{user};{url};{user_agent}\n'

        self.logfile = self.calc_logfile()
        with open(self.logfile, 'a') as f:
            f.write(log_txt)
        response = self.get_response(request)
        return response

    def timestamp(self):
        now = datetime.now()
        zmonth = str(now.month).zfill(2)
        zday = str(now.day).zfill(2)
        zhour = str(now.hour).zfill(2)
        zmin = str(now.minute).zfill(2)
        zsec = str(now.second).zfill(2)
        return f'{now.year}-{zmonth}-{zday} {zhour}:{zmin}:{zsec}'

    def filecalc_day(self):
        now = datetime.now()
        zmonth = str(now.month).zfill(2)
        zday = str(now.day).zfill(2)
        return f'{now.year}-{zmonth}-{zday}'

    def calc_logfile(self) -> str:
        result = None
        logdir = config('LOGDIR', default=None)
        if logdir is None:
            # determine temp dir
            import tempfile
            logdir = tempfile.gettempdir()
        # determine log file name from date
        now = datetime.now()
        logfilename = f'{self.filecalc_day()}.log'
        result = os.path.join(logdir, logfilename)
        return result


    def log_req(self, request):
        rem_addr = request.META.get('REMOTE_ADDR')
        user = request.user

        referer = request.META.get('HTTP_REFERER')
        querystring = request.META.get("QUERY_STRING")
        if querystring is None:
            querystring = ''
        else:
            querystring = '?' + querystring
        url = referer + querystring

        log_txt = f'{self.timestamp()} {rem_addr} {user} {url}\n'

        logfile = self.calc_logfile()
        with open(logfile, 'a') as f:
            f.write(log_txt)
            f.flush()
        return {}
