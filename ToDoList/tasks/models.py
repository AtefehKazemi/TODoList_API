from django.db import models
from django.contrib.auth.models import User
from user_groups.models import group_user
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver


class task(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=30)
    task_groups = models.ManyToManyField(group_user, null=True, blank=True)
    description = models.TextField(blank=True, default='')
    due_date = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def remain_days(self):
        remained_days = self.due_date - timezone.now()
        return f"{remained_days.days} days"


@receiver(pre_save, sender=task)
def check_values(sender, instance, **kwargs):
    if instance.due_date <= timezone.now():
        raise Exception("The Due date must be in the future.")