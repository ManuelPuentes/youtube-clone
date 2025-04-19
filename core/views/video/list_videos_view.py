from django.shortcuts import render
from django.views import View
from core.services.video.youtube_service import YoutubeService


class ListVideosView(View):

    def __init__(self, youtube_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()

    def get(self, request):

        page_token = request.GET.get('page', None)
        response = self.youtube_service.popular_videos(
            max_results=24, page_token=page_token)

        context = {
            'videos': response.get('videos'),
            'next_page_token': response.get('next_page_token'),
            'prev_page_token': response.get('next_page_token')
        }

        return render(request, 'partials/list_videos.html', {
            'data': context
        })
