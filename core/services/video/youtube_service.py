from googleapiclient.discovery import build
from django.conf import settings
import isodate


class YoutubeService():

    def __init__(self):
        self.youtube = build(
            'youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    def popular_videos(self, max_results=10, page_token=None):

        request = self.youtube.videos().list(
            part="id,snippet,statistics,contentDetails",
            chart="mostPopular",
            maxResults=max_results,
            pageToken=page_token,
        )

        request.headers["referer"] = "http://localhost"

        response = request.execute()

        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['id'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channelTitle': item['snippet']['channelTitle'],
                'url': f'https://www.youtube.com/watch?v={item['id']}',
                'views': self._format_number(int(item['statistics']['viewCount'])),
                'duration': self._format_video_duration(item['contentDetails']['duration'])
            })

        return {
            'videos': videos,
            'next_page_token': response.get('nextPageToken'),
            'prev_page_token': response.get('prevPageToken')
        }

    def related_videos(self, category, max_results=10, page_token=None):

        request = self.youtube.videos().list(
            part="id,snippet,statistics,contentDetails",
            chart="mostPopular",
            videoCategoryId=category,
            maxResults=max_results,
            pageToken=page_token,
        )

        request.headers["referer"] = "http://localhost"

        response = request.execute()

        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['id'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channelTitle': item['snippet']['channelTitle'],
                'url': f'https://www.youtube.com/watch?v={item['id']}',
                'views': self._format_number(int(item['statistics']['viewCount'])),
                'duration': self._format_video_duration(item['contentDetails']['duration'])
            })

        return {
            'videos': videos,
            'next_page_token': response.get('nextPageToken'),
            'prev_page_token': response.get('prevPageToken')
        }

    def video_details(self, video_id):

        video_request = self.youtube.videos().list(
            part="id,snippet,statistics,contentDetails",
            id=video_id)

        video_request.headers["referer"] = "http://localhost"

        response_video = video_request.execute()

        item = response_video.get('items')[0]

        channel_request = self.youtube.channels().list(
            part="snippet,statistics",
            id=item['snippet']['channelId']
        )

        channel_request.headers["referer"] = "http://localhost"

        response_channel = channel_request.execute()

        channel = response_channel.get('items')[0]

        return {
            'id': item['id'],
            'title': item['snippet']['title'],
            'category': item['snippet']['categoryId'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'channel': {
                'title': channel['snippet']['title'],
                # 'url': channel['snippet']['customUrl'],
                'thumbnail': channel['snippet']['thumbnails']['high']['url'],
                'subscribers': self._format_number(int(channel['statistics']['subscriberCount'])),
            },
            'views': self._format_number(int(item['statistics']['viewCount'])),
            'duration': self._format_video_duration(item['contentDetails']['duration'])
        }

    def _format_video_duration(self, iso_duration):
        duration = isodate.parse_duration(iso_duration)
        horas = duration.seconds // 3600
        minutos = (duration.seconds % 3600) // 60
        segundos = duration.seconds % 60

        return f'{horas}:{minutos}:{segundos}'

    def _format_number(self, num):
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)
