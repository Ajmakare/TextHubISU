from ..DataStores.UserDataStore import *
from ..ServiceFiles.UserService import *
class UserController:
    
    def add_user_controller(request):
        return UserService.add_user_service(request)

