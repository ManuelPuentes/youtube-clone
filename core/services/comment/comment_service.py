from core.repositories.user_repository import UserRepository
from core.repositories.videos_repository import VideoRepository
from core.repositories.comments_repository import CommentRepository


class CommentService:
    def __init__(self):
        self.video_repo = VideoRepository()
        self.user_repo = UserRepository()
        self.comment_repo = CommentRepository()

    def create_comment(self, user, video_id, comment_content):

        video = self.video_repo.get_video(video_id)

        self.comment_repo.create_comment({
            'user': user,
            'video': video,
            'text': comment_content
        })

        return {
            'user': user.username,
            'comment': comment_content
        }
