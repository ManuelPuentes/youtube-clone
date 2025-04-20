from django.shortcuts import render
from django.views import View
from core.services.video.youtube_service import YoutubeService


class SearchVideosView(View):

    def __init__(self, youtube_service=None):
        super().__init__()
        self.youtube_service = youtube_service or YoutubeService()

    def get(self, request):

        page_token = request.GET.get('page', None)
        search_query = request.GET.get('q', '')

        print(page_token)
        print(search_query)

        try:
            response = self.youtube_service.search(
                max_results=1, page_token=page_token, search_query=search_query)
        except:
            print("hubo un error")

        # print(response)

        context = {
            # 'videos': response.get('videos'),
            'query': search_query,
            # 'next_page_token': response.get('next_page_token'),
            # 'prev_page_token': response.get('next_page_token')
        }

        return render(request, 'partials/search_videos.html', {'data': context})
