import json
from django.views import View
from django.http import JsonResponse
from core.services.video.video_service import VideoService
from core.services.vote.vote_service import VoteService
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class VideoVotesView(View):

    def __init__(self):
        super().__init__()
        self.video_service = VideoService()
        self.vote_service = VoteService()

    def get(self, request):
        video_id = request.GET.get('v')
        result = self.video_service.get_video_votes(request.user, video_id)

        return JsonResponse(result)

    @method_decorator(login_required)
    def put(self, request):

        data = json.loads(request.body)

        result = self.vote_service.create_vote(
            request.user,
            data.get('video_id'),
            data.get('vote')
        )

        return JsonResponse(result)
