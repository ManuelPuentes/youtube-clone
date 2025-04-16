from django import forms
from core.models import Video
from django.core.exceptions import ValidationError
import re

class VideoForm(forms.ModelForm):

    id = forms.CharField(
        label='Embeded link',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the video embed link'
        }),
        help_text='Link format: https://www.youtube.com/embed/CODIGO_DEL_VIDEO'
    )

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter the video embed link',
        'class': 'textarea'
    }),)

    thumbnail = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the video thumbnail link'
        }),
        help_text='Accepted formats: JPEG, PNG, GIF, SVG, or WebP.'
    )

    class Meta:
        model = Video
        fields = ['id', 'title', 'thumbnail', 'description']

    @staticmethod
    def extract_video_id(url):
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:embed\/|watch\?v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    def clean_id(self):
        id = self.cleaned_data.get('id')

        youtube_embed_pattern = r'^https?://(?:www\.)?(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})(?:\?.*)?$'

        if not re.match(youtube_embed_pattern, id):
            raise ValidationError(
                'link invalido'
            )

        video_id = self.extract_video_id(id)

        return video_id

    def clean_thumbnail(self):

        thumbnail = self.cleaned_data.get('thumbnail')

        thumbnail_url_pattern = r'^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w\- .\/]*)*\.(jpe?g|png|gif|webp|bmp|svg|ico)(\?.*)?$'

        if not re.match(thumbnail_url_pattern, thumbnail):
            raise ValidationError(
                'el thumbnail no es valido'
            )

        return thumbnail
