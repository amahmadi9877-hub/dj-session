from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.utils import timezone
from session.models import Session

SESSION_KEY = "_auth_user_id"
BACKEND_SESSION_KEY = "_auth_user_backend"
HASH_SESSION_KEY = "_auth_user_hash"
REDIRECT_FIELD_NAME = "next"


class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.session = Session()
        session_id = request.COOKIES.get("session_id")
        if (
            session_id
            and not request.path == "/register/"
            and not request.path == "/login/"
        ):
            try:
                request.session = Session.objects.get(session_id=session_id)
                if request.session.expire_date < timezone.now():
                    return redirect("login")
                request.user = request.session.user_id
            except Session.DoesNotExist:
                return redirect("login")

    # def process_response(self, request, response):
    #     if request.path == "/login/":
    #         session = Session.objects.create
