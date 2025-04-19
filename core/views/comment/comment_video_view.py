import json
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from core.services.comment.comment_service import CommentService
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CommentVideoView(View):

    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()

    def get(self, request):

        video_id = request.GET.get('v')

        # if video_id is None:
        #     return redirect('home')

        page_number = request.GET.get('page', 1)

        print(page_number)

        paginator = Paginator(self.comment_service.get_comments(video_id), 5)
        page_obj = paginator.get_page(page_number)

        return render(request, 'articles.html', {'comments': page_obj})

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
