from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator
from core.services.video.video_service import VideoService
from core.services.video.youtube_service import YoutubeService
from core.services.comment.comment_service import CommentService


class WatchVideoView(View):

    def __init__(self, youtube_service=None, video_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()
        self.video_service = video_service or VideoService()
        self.comment_service = CommentService()

    def get(self, request):
        video_id = request.GET.get('v')

        if video_id is None:
            return redirect('home')

        response = self.youtube_service.video_details(video_id)

        if response.get('error'):
            error = response.get('error')

            return render(request, 'error.html', {
                'error_message': response.get('message'),
                'error_code': error.resp.status,
                'error_details': error.error_details if hasattr(error, 'error_details') else None
            })

        self.video_service.create_video_if_needed(response.get('video'))

        return render(request, 'watch.html', {
            'video_data': response.get('video'),
        })
