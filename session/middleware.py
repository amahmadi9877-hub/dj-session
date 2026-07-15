import time
from django.utils.deprecation import MiddlewareMixin
from session.sessionstore import SessionStore
from django.utils.http import http_date
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.exceptions import SessionInterrupted


class SessionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.SessionStore = SessionStore

    def process_request(self, request):
        session_key = request.COOKIES.get("session_key")
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        try:
            empty = request.session.is_empty()
        except AttributeError:
            return response
        if "session_key" in request.COOKIES and empty:
            response.delete_cookie("session_key")
        else:
            if not empty:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = http_date(expires_time)
                if response.status_code < 500:
                    try:
                        request.session.save()
                    except UpdateError:
                        raise SessionInterrupted(
                            "The request's session was deleted before the "
                            "request completed. The user may have logged "
                            "out in a concurrent request, for example."
                        )
                    response.set_cookie(
                        "session_key",
                        request.session._session_key,
                        max_age=max_age,
                        expires=expires,
                    )

                    # "https://youtube.com/@ramin-s?si=NC9LTub6LoVYLLc2"

        return response
