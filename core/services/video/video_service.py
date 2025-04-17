from core.models import Vote
from core.repositories.user_repository import UserRepository
from core.repositories.videos_repository import VideoRepository


class VideoService:
    def __init__(self):
        self.video_repo = VideoRepository()
        self.user_repo = UserRepository()

    def create_video(self, video):
        video = self.video_repo.create_video(video)
        result = True if video is not None else False

        return result, video

    def create_video_if_needed(self, video_data):
        channel_data = video_data.get('channel')

        user, _created = self.user_repo.get_or_create_user(
            f'custom_email{channel_data.get('title')}.com',
            {
                'username': f'{channel_data.get('title')}',
                'first_name': 'default_first_name',
                'last_name': 'default_last_name',
                'password': 'default_password'
            }
        )

        video, _video_created = self.video_repo.get_or_create_video(
            f'{video_data.get('id')}',
            {
                'title': f'{video_data.get('title')}',
                'description': f'{video_data.get('description')}',
                'thumbnail': f'{video_data.get('thumbnail')}',
                'uploader_id': f'{user.id}'
            }
        )

        return video

    def get_video(self, video_id):
        return self.video_repo.get_video(video_id)

    def get_video_votes(self, user, video_id):

        video = self.video_repo.get_video(video_id)

        user_vote = None

        if user.is_authenticated:
            user_vote = Vote.objects.filter(
                user=user,
                video=video,
            ).first()

        return {
            'total_likes': video.total_likes,
            'total_dislikes': video.total_dislikes,
            'user_vote': user_vote.like_dislike if user_vote is not None else None
        }
