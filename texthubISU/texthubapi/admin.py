from django.contrib import admin

# Register your models here.

from .models import Textbook
admin.site.register(Textbook)

from .models import Source
admin.site.register(Source)

from .models import Review
admin.site.register(Review)

from .models import Feedback
admin.site.register(Feedback)

from .models import Request
admin.site.register(Request)