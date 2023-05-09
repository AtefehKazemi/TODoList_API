from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class group_user(models.Model):
    author = models.ForeignKey(User, related_name= 'created_group_user', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User, related_name= 'group_user')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    def number_of_members(self):
        return self.members.count()

    def get_username(self):
        return self.author.username


# if the author is not in members while creating or editing a group_user instance
# we add him to m2m field by using this signal
@receiver(m2m_changed, sender = group_user.members.through)
def  group_user_members_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action is 'pre_add':
        if instance.author.id not in pk_set:
            pk_set.add(instance.author.id)
    elif action is 'pre_remove':
        if instance.author.id in pk_set:
            pk_set.remove(instance.author.id)
