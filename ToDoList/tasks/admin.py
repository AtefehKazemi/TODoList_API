from django.contrib import admin
from .models import task, comment, notification, group_user


admin.site.register(task)
admin.site.register(comment)
admin.site.register(notification)
admin.site.register(group_user)




