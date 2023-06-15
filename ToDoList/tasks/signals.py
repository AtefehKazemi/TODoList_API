from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import group_user, notification, task
from django.contrib.auth.models import User


# if the creator of group is not in members while creating or editing a group_user instance
# we add him to m2m field by using this signal
# also notifications are created for added or removed members
@receiver(m2m_changed, sender = group_user.members.through)
def  group_user_members_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action is 'pre_add':
        if instance.creator.id not in pk_set:
            pk_set.add(instance.creator.id)
    elif action is 'pre_remove':
        if instance.creator.id in pk_set:
            pk_set.remove(instance.creator.id)
    elif action is 'post_add':
        for i in pk_set:
            if  i != instance.creator.id:
                notification_instance = notification.objects.create(receiver=User.objects.get(id = i), is_read=False,
                                                                message='You are added to group ' + instance.name)
                notification_instance.save()
    elif action == "post_remove":
        for i in pk_set:
            if  i != instance.creator.id:
                notification_instance = notification.objects.create(receiver=User.objects.get(id = i), is_read=False,
                                                                    message='You are removed from group ' + instance.name)
                notification_instance.save()


'''
<<<<WORK ON IT LATER>>>
@receiver(m2m_changed, sender = task.task_groups.through)
def task_task_groups_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action is 'post_add':
        for i in pk_set:
            for user_id in group_user.objects.get(id=i).members:
                notification_instance = notification.objects.create(receiver=User.objects.get(id=user_id), is_read=False,
                                                                message='You are added to task ' + instance.title)
                notification_instance.save()
    elif action == "post_remove":
        for i in pk_set:
            for user_id in group_user.objects.get(id=i).members:
                notification_instance = notification.objects.create(receiver=User.objects.get(id=user_id), is_read=False,
                                                                    message='You are removed from task ' + instance.title)
                notification_instance.save()
                '''
