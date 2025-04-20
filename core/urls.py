from django.urls import path

from core.views.home import HomeView
from core.views.auth.signin_view import SignInView
from core.views.auth.signout_view import SignOutView
from core.views.auth.register_view import RegisterView
from core.views.video.video_votes import VideoVotesView
from core.views.video.watch_view import WatchVideoView
from core.views.video.list_videos_view import ListVideosView
from core.views.video.upload_video_view import UploadVideoView
from core.views.comment.comment_video_view import CommentVideoView
from core.views.video.related_videos_view import RelatedVideosViews
from core.views.video.search_videos_view import SearchVideosView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # auth
    path('signin/', SignInView.as_view(), name='signin'),
    path('accounts/login/', SignInView.as_view(), name='signin_required'),
    path('register/', RegisterView.as_view(), name='register'),
    path('signout/', SignOutView.as_view(), name='logout'),

    # videos
    path('list_videos/', ListVideosView.as_view(), name='list_videos'),
    path('watch/', WatchVideoView.as_view(), name='watch'),
    path('comment/', CommentVideoView.as_view(), name='comment_video'),
    path('upload_video/', UploadVideoView.as_view(), name='upload'),
    path('related_videos/', RelatedVideosViews.as_view(), name='related_videos'),
    path('video/vote/', VideoVotesView.as_view(), name='video_votes'),



    path('search', SearchVideosView.as_view(), name='search'),
]
