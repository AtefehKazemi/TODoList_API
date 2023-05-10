from rest_framework import serializers
from .models import task, comment, notification, group_user
from django.utils import timezone

# task serializers:

def validate_due_date(value):
    if value <= timezone.now():
        raise serializers.ValidationError("Due date : The Due date must be in the future.")
    return value


class subtask_form(serializers.ModelSerializer):
    remained_days = serializers.SerializerMethodField(method_name = 'get_remained_days')
    class Meta:
        model = task
        fields = ['id', 'title', 'due_date', 'remained_days']

    def get_remained_days(self, obj):
        return obj.remain_days()


class task_serializer_detail_edit(serializers.ModelSerializer):
    remained_days = serializers.SerializerMethodField(method_name = 'get_remained_days')
    due_date = serializers.DateTimeField(validators=[validate_due_date])
    subtasks = subtask_form(many=True, read_only=True)
    class Meta:
        model = task
        fields = ['id', 'parent', 'author', 'title', 'task_groups', 'description', 'subtasks', 'due_date', 'remained_days', 'created_at', 'updated_at']

    def get_remained_days(self, obj):
        return obj.remain_days()


class task_create_serializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(validators=[validate_due_date])
    class Meta:
        model = task
        fields = ['id', 'parent', 'title', 'task_groups', 'description', 'due_date']


# comment serializers:

# used for viewing a comment's details
class comment_serializer_view(serializers.ModelSerializer):
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author_username = serializers.SerializerMethodField()
    # reply_count = serializers.SerializerMethodField()

    class Meta:
        model = comment
        fields = ('id', 'author', 'author_username', 'content', 'related_task', 'parent', 'replies', 'created_at')

    def get_author_username(self, obj):
        return obj.get_username()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reply_count'] = instance.replies.count()
        return representation

    '''
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
        '''


# used for creating and editing comments
class comment_serializer_create_and_edit(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ('id','content','related_task', 'parent', 'created_at')


# user_groups serializer:

class group_user_serializer(serializers.ModelSerializer):
    creator_username = serializers.SerializerMethodField()

    class Meta:
        model = group_user
        fields = '__all__'
        read_only = ('creator',)
        include = ('creator_username',)

    def get_creator_username(self, obj):
        return obj.get_username()
    

# notification serializers:

class notification_serializer(serializers.ModelSerializer):

    class Meta:
        model = notification
        fields = '__all__'