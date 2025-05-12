from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from two_factor.views import LoginView

class CustomLoginView(LoginView):
    def get_redirect_url(self):
        # Redirect to 'next' URL or default to admin dashboard
        return self.request.POST.get('next', '/admin/')