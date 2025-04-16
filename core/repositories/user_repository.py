from django.core.exceptions import ObjectDoesNotExist
from core.models import CustomUser


class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_user(user_data):
        return CustomUser.objects.create_user(**user_data)

    @staticmethod
    def get_or_create_user(email, defaults):
        return CustomUser.objects.get_or_create(email=email, defaults=defaults)

    @staticmethod
    def update_user(user, update_data):
        for key, value in update_data.items():
            setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def email_exists(email):
        return CustomUser.objects.filter(email=email).exists()
