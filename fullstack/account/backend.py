from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Пытается пройти аутентификацию username с password с помощью check_password().
        """
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        if email is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user
