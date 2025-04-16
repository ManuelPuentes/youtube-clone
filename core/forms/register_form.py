from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm

from core.models import CustomUser

class RegisterForm(UserCreationForm):

    username = forms.CharField(
        label='Your Username',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter a unique username'
        }),
        help_text=''
    )

    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(),
        help_text=mark_safe("""
                Requisitos de contraseña:<br>
                - Mínimo 8 caracteres<br>
                - No puede ser similar a tu nombre de usuario<br>
                - No puede ser completamente numérica<br>
                - No puede ser una contraseña común
        """)
    )

    password2 = forms.CharField(
        label='Password confirmation:',
        required=True,
        widget=forms.PasswordInput(),
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get(
            'email').lower()  # Normaliza a minúsculas
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado")
        return email

