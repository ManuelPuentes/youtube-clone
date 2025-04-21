from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
import isodate
from decouple import config

from core.utils.data_class.video_data import ChannelData, VideoData


class YoutubeService():

    def __init__(self):
        self.youtube = build(
            'youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    def _make_request(self, endpoint, **kwargs):
        request = getattr(self.youtube, endpoint)().list(**kwargs)
        request.headers["referer"] = settings.REFERER
        return request.execute()

    def popular_videos(self, max_results=10, page_token=None):

        try:

            response = self._make_request(
                'videos',
                part="id,snippet,statistics,contentDetails",
                chart="mostPopular",
                maxResults=max_results,
                pageToken=page_token,
            )

            videos = []
            for item in response.get('items', []):

                if video := VideoData.from_videos_api_response(item):
                    videos.append(video)

            return {
                'videos': videos,
                'next_page_token': response.get('nextPageToken'),
                'prev_page_token': response.get('prevPageToken')
            }

        except HttpError as error:
            return {'message':  self.handle_youtube_api_errors(error), 'error': error}

    def related_videos(self, category, max_results=10, page_token=None):

        try:

            response = self._make_request(
                'videos',
                part="id,snippet,statistics,contentDetails",
                chart="mostPopular",
                videoCategoryId=category,
                maxResults=max_results,
                pageToken=page_token,
            )

            videos = []
            for item in response.get('items', []):

                if video := VideoData.from_videos_api_response(item):
                    videos.append(video)

            return {
                'videos': videos,
                'next_page_token': response.get('nextPageToken'),
                'prev_page_token': response.get('prevPageToken')
            }
        except HttpError as error:
            return {'message':  self.handle_youtube_api_errors(error), 'error': error}

    def video_details(self, video_id):

        try:

            video = self.get_first_item(self._make_request(
                'videos',
                part="id,snippet,statistics,contentDetails",
                id=video_id
            ))

            video_data = VideoData.from_videos_api_response(video)

            channel = self.get_first_item(self._make_request(
                'channels',
                part="snippet,statistics",
                id=video_data.channel.id
            ))

            video_data.channel = ChannelData.from_api_response(channel)

            return {'video': video_data, 'success': True}

        except HttpError as error:
            return {'message':  self.handle_youtube_api_errors(error), 'error': error}
        except ValueError as error:
            return {'message':  'elemento no encontrado', 'error': error}

    def search(self, max_results=10, search_query='', page_token=None):

        try:
            search_response = self._make_request(
                'search',
                part="id,snippet",
                q=search_query,
                maxResults=max_results,
                pageToken=page_token,
                type="video",    # Puedes especificar el tipo: video, channel, playlist
                order="relevance"  # Otros valores: date, rating, viewCount
            )

            video_ids = [item['id']['videoId']
                         for item in search_response['items']]

            videos_response = self._make_request(
                'videos',
                part="id,snippet,statistics,contentDetails",
                maxResults=max_results,
                id=",".join(video_ids)
            )

            videos = []
            for item in videos_response.get('items', []):

                if video := VideoData.from_videos_api_response(item):
                    videos.append(video)

            return {
                'videos': videos,
                'next_page_token': search_response.get('nextPageToken'),
                'prev_page_token': search_response.get('prevPageToken')
            }

        except HttpError as e:
            print(e)
            return {'message':  self.handle_youtube_api_errors(e), 'error': e}

    def handle_youtube_api_errors(self, error):
        return error.error_details[0]['message'] if error.error_details[0]['message'] else None

    def get_first_item(self, api_response):
        try:
            if not api_response.get('items'):
                raise ValueError(
                    "El response no contiene elementos en 'items'")

            first_item = api_response['items'][0]
            return first_item

        except (KeyError, IndexError) as e:
            raise ValueError("No se pudo obtener el elemento") from e
