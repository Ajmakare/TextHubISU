class UserDataStore:
    def add_user(user):
        try:
            user.save()
        except:
            return "Could not add user"