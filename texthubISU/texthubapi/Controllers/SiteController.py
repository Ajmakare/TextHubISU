from ..ServiceFiles.SiteService import *
class SiteController:
        
    def submit_feedback_controller(request):
        return SiteService.submit_feedback_service(request)
