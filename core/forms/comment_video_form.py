from django import forms
from core.models import Comment
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Añade un comentario...',
        'class': 'textarea'
    }),)

    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):

        text = self.cleaned_data.get('text')

        if text is '':
            raise ValidationError(
                'empty comment message cant be posted'
            )

        return text
