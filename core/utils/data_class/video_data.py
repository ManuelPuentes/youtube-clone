from dataclasses import dataclass
from typing import Optional
import isodate


@dataclass
class ChannelData:
    id: str
    name: str
    url: Optional[str]
    thumbnail: Optional[str]
    subscribers: Optional[int]

    @classmethod
    def from_video_data(cls, item: dict) -> Optional['ChannelData']:
        try:
            return cls(
                id=item.get('id', ''),
                name=item.get('name', ''),
                url='',
                thumbnail='',
                subscribers=0
            )
        except Exception as e:
            print(f"Error al crear Channel: {e}")
            return None

    @classmethod
    def from_api_response(cls, item: dict) -> Optional['ChannelData']:

        try:
            return cls(
                id=item.get('id', ''),
                name=item.get('snippet', {}).get('title', ''),
                url=item.get('snippet', {}).get('customUrl', ''),
                thumbnail=item.get('snippet', {}).get(
                    'thumbnails', {}).get('high', {}).get('url', ''),
                subscribers=_format_number(int(item.get('statistics', {}).get(
                    'subscriberCount', 0)))
            )
        except Exception as e:
            print(f"Error al crear Video: {e}")
            return None

# video data class holds data fetch from youtube api, the initializers methods follows these naming rule: from_(endpoint_name)_api_response, these is becasuse depending the method youtube returns diferent formats but our app wants to unify them 
@dataclass
class VideoData:
    id: str
    title: str
    thumbnail: str
    # channel_title: str
    description: str
    category: str
    views: str
    duration: str
    url: str
    channel: Optional[ChannelData] = None  # Campo opcional

    @classmethod
    def from_videos_api_response(cls, item: dict) -> Optional['VideoData']:
        try:
            return cls(
                id=item.get('id', ''),
                title=item.get('snippet', {}).get('title', 'Sin título'),
                url=f'https://www.youtube.com/watch?v={item.get('id', '')}',
                category=item.get('snippet', {}).get('categoryId', ''),
                description=item.get('snippet', {}).get(
                    'description', 'Sin descripcion'),
                thumbnail=item.get('snippet', {}).get(
                    'thumbnails', {}).get('high', {}).get('url', ''),
                views=_format_number(
                    int(item.get('statistics', {}).get('viewCount', 0))),
                duration=_format_video_duration(
                    item.get('contentDetails', {}).get('duration', '')),

                channel=ChannelData.from_video_data({
                    'id': item.get('snippet', {}).get('channelId', 'Sin Nombre'),
                    'name': item.get('snippet', {}).get('channelTitle', '')
                })

            )
        except Exception as e:
            print(f"Error al crear Video: {e}")
            return None

       
    
    @classmethod
    def from_search_api_response(cls, item: dict) -> Optional['VideoData']:

        try:
            return cls(
                id=item.get('id', {}).get('videoId', ''),
                title=item.get('snippet', {}).get('title', 'Sin título'),
                url=f'https://www.youtube.com/watch?v={item.get('id', '')}',
                category=item.get('snippet', {}).get('categoryId', ''),
                description=item.get('snippet', {}).get(
                    'description', 'Sin descripcion'),
                thumbnail=item.get('snippet', {}).get(
                    'thumbnails', {}).get('high', {}).get('url', ''),
                views= '0',
                duration='',
                channel=ChannelData.from_video_data({
                    'id': item.get('snippet', {}).get('channelId', 'Sin Nombre'),
                    'name': item.get('snippet', {}).get('channelTitle', '')
                })

            )
        except Exception as e:
            print(f"Error al crear Video: {e}")
            return None


def _format_video_duration(iso_duration):
    duration = isodate.parse_duration(iso_duration)
    horas = duration.seconds // 3600
    minutos = (duration.seconds % 3600) // 60
    segundos = duration.seconds % 60

    return f'{horas}:{minutos}:{segundos}'


def _format_number(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
