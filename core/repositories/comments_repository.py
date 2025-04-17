from core.models import Comment


class CommentRepository:

    @staticmethod
    def get_all_comments(video_id):
        try:
            comments = Comment.objects.filter(video_id=video_id).order_by('-created_at')
        except Exception as e:
            comments = None

        return comments

    @staticmethod
    def create_comment(comment_data):
        try:
            comment = Comment.objects.create(**comment_data)
        except Exception as e:
            comment = None

        return comment
