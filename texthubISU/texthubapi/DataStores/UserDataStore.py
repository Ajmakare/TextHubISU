from django.contrib.auth.models import User


class UserDataStore:
    def add_user(user):
        try:
            user.save()
        except:
            return "Could not add user"

    def read_user(username2):
        try:
            User2 = User.objects.get(username=username2)
            return User2
        except:
            return "Could not access user"
