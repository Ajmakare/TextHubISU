from ..ServiceFiles.SiteService import *
class SiteController:
        
    def submit_feedback_controller(request):
        SiteService.submit_Feedback_service(request)
        pass