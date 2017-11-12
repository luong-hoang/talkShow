from django.contrib import admin
from .models import User, Subject, TalkShow, TalkShowSubject

# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(TalkShow)
admin.site.register(TalkShowSubject)

