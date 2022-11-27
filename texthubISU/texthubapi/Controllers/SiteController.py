from ..ServiceFiles.SiteService import *
class SiteController:
        
    def submit_feedback_controller(request):
        return SiteService.submit_Feedback_service(request)
        # pass