class AdminDatastore:

    def add_admin(admin_credentials):
        try:
            admin_credentials.save()
        except:
            return "Could not request an ISBN"

    def login():
        pass