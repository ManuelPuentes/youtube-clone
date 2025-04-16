from ...repositories.user_repository import UserRepository
from django.contrib.auth import login, authenticate, logout


class AuthService:
    def __init__(self, request=None):
        self.request = request
        self.user_repo = UserRepository()

    def register_user(self, user):
        try:
            user = self.user_repo.create_user(user)
            self._perform_login(user)
            return True, user
        except Exception as e:
            return False

    def signin_user(self, data):

        user = authenticate(
            self.request, username=data.get('username'), password=data.get('password'))

        if user is not None:
            self._perform_login(user)
            return True

        return False

    def signout_user(self):
        if self.request:
            logout(self.request)

    def _perform_login(self, user):
        if self.request:
            login(self.request, user)
