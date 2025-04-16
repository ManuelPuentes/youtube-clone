from core.models import Comment


class CommentRepository:
    @staticmethod
    def create_comment(comment_data):
        try:
            comment = Comment.objects.create(**comment_data)
        except Exception as e:
            comment = None

        return comment
