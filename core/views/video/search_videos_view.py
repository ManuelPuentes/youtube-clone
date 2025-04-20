from django.shortcuts import render
from django.views import View
from core.services.video.youtube_service import YoutubeService
from googleapiclient.errors import HttpError


class SearchVideosView(View):

    def __init__(self, youtube_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()

    def get(self, request):

        is_htmx = request.headers.get('HX-Request') == 'true'
        page_token = request.GET.get('page', None)
        search_query = request.GET.get('q', '')

        if is_htmx:
            response = self.youtube_service.search(
                max_results=5, page_token=page_token, search_query=search_query)

            if response.get('error'):
                error = response.get('error')

                return render(request, 'error.html', {
                    'error_code': error.resp.status,
                    'error_details': error.error_details if hasattr(error, 'error_details') else None
                })

            context = {
                'videos': response.get('videos'),
                'query': search_query,
                'next_page_token': response.get('next_page_token'),
                'prev_page_token': response.get('next_page_token')
            }
            return render(request, 'partials/search_videos.html', {'data': context})

        else:
            return render(request, 'search.html', {'data': {'query': search_query}})
