from django.views import View
from django.shortcuts import redirect
from core.services.auth.auth_service import AuthService

class SignOutView(View):
    def get(self, request):
        auth_service = AuthService(request)
        auth_service.signout_user()
        return redirect('home')
