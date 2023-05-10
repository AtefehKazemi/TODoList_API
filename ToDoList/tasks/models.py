from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class group_user(models.Model):
    creator = models.ForeignKey(User, related_name= 'created_group_user', on_delete=models.CASCADE , editable = False)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User, related_name= 'group_user')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    def number_of_members(self):
        return self.members.count()

    def get_username(self):
        return self.creator.username
    

class task(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subtasks', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE, editable = False)
    title = models.CharField(max_length=30)
    task_groups = models.ManyToManyField(group_user, blank=True)
    description = models.TextField(blank=True, default='')
    due_date = models.DateTimeField(auto_now_add=False, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def remain_days(self):
        remained_days = self.due_date - timezone.now()
        return f"{remained_days.days} days"


class comment(models.Model):
    related_task = models.ForeignKey(task, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name = 'replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE , editable = False)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.related_task}'

    def get_username(self):
        return self.author.username

    '''
    # returns a comment(self) children ids
    def children(self):
        return comment.objects.filter(parent=self)

    # if a comment(self) has replies it returns True
    # else returns False
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
        '''
    

class notification(models.Model):
    receiver = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ('-timestamp',)

    def __str__(self):
        return self.receiver.username