from django.shortcuts import redirect, render
from django.views import View
from core.forms.upload_video_form import VideoForm
from core.services.video.video_service import VideoService
from core.services.video.youtube_service import YoutubeService
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UploadVideoView(View):

    def __init__(self, youtube_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()

    @method_decorator(login_required)
    def get(self, request):
        form = VideoForm()
        return render(request, 'upload.html', {'upload_form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = VideoForm(request.POST)

        if form.is_valid():

            video_service = VideoService(request)

            video = {
                'id': form.cleaned_data.get('id'),
                'title': form.cleaned_data.get('title'),
                'thumbnail': form.cleaned_data.get('thumbnail'),
                'description': form.cleaned_data.get('description'),
                'uploader':  request.user
            }

            success = video_service.create_video(video)

            if (success):
                return redirect(f'/watch?v={video.get('id')}')
            else:
                form.add_error(None, "video upload unexpected error.")

        return render(request, 'upload.html', {'upload_form': form})
