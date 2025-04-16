from core.models import Video


class VideoRepository:

    @staticmethod
    def get_video(video_id):

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            video = None

        return video

    @staticmethod
    def get_or_create_video(id, defaults):
        return Video.objects.get_or_create(id=id, defaults=defaults)
    
    @staticmethod
    def create_video(video_data):

        try:
            video = Video.objects.create(**video_data)
        except Exception as e:
            video = None

        return video
