from django.shortcuts import redirect, render
from django.views import View
from core.services.video.video_service import VideoService
from core.services.video.youtube_service import YoutubeService


class WatchVideoView(View):

    def __init__(self, youtube_service=None, video_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()
        self.video_service = video_service or VideoService()

    def get(self, request):
        video_id = request.GET.get('v')

        if video_id is None:
            return redirect('home')

        video_data = self.youtube_service.video_details(video_id)

        self.video_service.create_video_if_needed(video_data)

        related_videos = self.youtube_service.related_videos(
            video_data.get('category'), 10)['videos']

        return render(request, 'watch.html', {'video_data': video_data, 'related_videos': related_videos, })
