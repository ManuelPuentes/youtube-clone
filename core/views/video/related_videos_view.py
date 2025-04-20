from django.shortcuts import render
from django.views import View
from core.services.video.youtube_service import YoutubeService


class RelatedVideosViews(View):

    def __init__(self, youtube_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()

    def get(self, request):

        video_category = request.GET.get('category')

        page_token = request.GET.get('page', None)

        response = self.youtube_service.related_videos(
            video_category, 10, page_token)

        if response.get('error'):
            error = response.get('error')

            return render(request, 'error.html', {
                'error_message': response.get('message'),
                'error_code': error.resp.status,
                'error_details': error.error_details if hasattr(error, 'error_details') else None
            })

        context = {
            'related_videos': response.get('videos'),
            'next_page_token': response.get('next_page_token'),
            'prev_page_token': response.get('next_page_token'),
            'video_category': video_category
        }

        return render(request, 'partials/related_videos.html', {
            'data': context
        })
