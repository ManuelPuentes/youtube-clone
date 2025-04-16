from django.views import View
from django.shortcuts import render, redirect
from core.forms.signin_form import CustomAuthenticationForm
from core.services.auth.auth_service import AuthService


class SignInView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('home')

        form = CustomAuthenticationForm()
        return render(request, 'auth/signin.html', {'signin_form': form})

    def post(self, request):

        next = request.GET.get('next')

        form = CustomAuthenticationForm(request=request, data=request.POST)

        if form.is_valid():

            auth_service = AuthService(request)
            success = auth_service.signin_user({
                'username': form.cleaned_data.get('username'),
                'password': form.cleaned_data.get('password')
            })

            if (success and next):
                return redirect(next)
            elif (success):
                return redirect('home')
            else:
                form.add_error(None, "username or password is incorrect.")

        return render(request, 'auth/signin.html', {'signin_form': form})
