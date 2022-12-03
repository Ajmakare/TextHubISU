from django.contrib.auth.models import User


class UserDataStore:
    def add_user(username, email, password):
        try:
            User.objects.create_user(username=username,
                password=password,email=email)
        except:
            raise AttributeError

    def read_user(username2):
        try:
            User2 = User.objects.get(username=username2)
            return User2
        except:
            return "Could not access user"
