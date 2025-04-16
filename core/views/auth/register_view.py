from django.views import View
from django.shortcuts import render, redirect
from core.forms.register_form import RegisterForm
from core.services.auth.auth_service import AuthService


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = RegisterForm()
        return render(request, 'auth/register.html', {'register_form': form})

    def post(self, request):

        form = RegisterForm(request.POST)

        if form.is_valid():

            auth_service = AuthService(request)

            user = {
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'password': form.cleaned_data.get('password1'),
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
            }

            success = auth_service.register_user(user)

            if (success):
                return redirect('home')
            else:
                form.add_error(None, "Register failed try again")

        return render(request, 'auth/register.html', {
            'register_form': form,
        })
