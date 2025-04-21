from core.models import Vote
from core.repositories.user_repository import UserRepository
from core.repositories.videos_repository import VideoRepository
from core.utils.data_class.video_data import VideoData


class VideoService:
    def __init__(self):
        self.video_repo = VideoRepository()
        self.user_repo = UserRepository()

    def create_video(self, video):
        video = self.video_repo.create_video(video)
        result = True if video is not None else False

        return result, video

    def create_video_if_needed(self, video_data: VideoData):

        user, _created = self.user_repo.get_or_create_user(
            f'custom_email{video_data.channel.name}.com',
            {
                'username': f'{video_data.channel.name}',
                'first_name': 'default_first_name',
                'last_name': 'default_last_name',
                'password': f'{video_data.channel.name}_password'
            }
        )

        video, _video_created = self.video_repo.get_or_create_video(
            f'{video_data.id}',
            {
                'title': f'{video_data.title}',
                'description': f'{video_data.description}',
                'thumbnail': f'{video_data.thumbnail}',
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
