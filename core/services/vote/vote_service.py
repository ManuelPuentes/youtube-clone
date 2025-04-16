from core.models import Vote
from core.repositories.user_repository import UserRepository
from core.repositories.videos_repository import VideoRepository


class VoteService:
    def __init__(self):
        self.video_repo = VideoRepository()
        # self.video_repo = VideoRepository()

    def get_votes(self):
        return True

    def create_vote(self, user, video_id, user_vote):

        video = self.video_repo.get_video(video_id)

        vote, created = Vote.objects.get_or_create(
            user=user,
            video=video,
            defaults={'like_dislike':  user_vote}
        )

        if not created:
            if vote.like_dislike != user_vote:
                vote.like_dislike = user_vote
                vote.save()
            else:
                vote.delete()
                user_vote = None

        return {
            'total_likes': video.total_likes,
            'total_dislikes': video.total_dislikes,
            'user_vote': user_vote
        }
