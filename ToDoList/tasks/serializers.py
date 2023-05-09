from rest_framework import serializers
from .models import task


class task_serializer(serializers.ModelSerializer):
    remained_days = serializers.SerializerMethodField(method_name = 'get_remained_days')

    class Meta:
        model = task
        fields = ['id', 'parent', 'author', 'title', 'task_groups', 'description', 'due_date', 'remained_days', 'created_at', 'updated_at']

    def get_remained_days(self, obj):
        return obj.remain_days()


class task_create_serializer(serializers.ModelSerializer):

    class Meta:
        model = task
        fields = ['id', 'parent', 'title', 'task_groups', 'description', 'due_date', 'created_at', 'updated_at']