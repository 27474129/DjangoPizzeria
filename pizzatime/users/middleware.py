from django.shortcuts import redirect
from django.urls import reverse_lazy



class AuthCheckingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if ("user_id" in request.session and request.path == reverse_lazy("auth")):
            return redirect("index")

        response = self.get_response(request)
        return response
