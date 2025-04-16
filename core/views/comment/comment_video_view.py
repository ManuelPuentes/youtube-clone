import json
from django.views import View
from django.http import JsonResponse
from core.services.comment.comment_service import CommentService
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CommentVideoView(View):

    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()

    @method_decorator(login_required)
    def post(self, request):

        data = json.loads(request.body)

        result = self.comment_service.create_comment(
            request.user,
            data.get('video_id'),
            data.get('comment_content')
        )

        return JsonResponse({
            'success': True,
            'data': result
        })
