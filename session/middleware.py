from django.utils.deprecation import MiddlewareMixin


class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/login/":
            print("login request")
        elif request.path == "/register/":
            print("register request")
        elif request.path == "/show/":
            print("show request")
