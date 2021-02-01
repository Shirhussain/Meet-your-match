from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.shortcuts import HttpResponseRedirect


URLS = [reverse(url) for url in settings.SUBSCRIPTION_REQUIRED_URLS]

class CheckMembership:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.user.is_authenticated:
            # messages.success(request, "user is logged in ")
            if request.path in URLS:
                role = request.user.userrole
                if str(role) != "Staff  ":
                    messages.success(request, f"you need to upgrade your membership plan to see that, your rol is: {role}")
                    return HttpResponseRedirect(reverse("home"))
        else:
            messages.success(request, "user is not logged in")
            print("not logged in horraaaaaaaaaaaaaaaaaaaaaa")