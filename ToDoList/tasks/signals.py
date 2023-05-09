from .models import task
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(pre_save, sender=task)
def check_values(sender, instance, **kwargs):
    if instance.due_date <= timezone.now():
        raise Exception("The Due date must be in the future")