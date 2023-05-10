from django.contrib import admin
from .models import task, comment

# Register your models here.

admin.site.register(task)
admin.site.register(comment)

