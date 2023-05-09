from rest_framework import serializers
from .models import group_user


class group_user_serializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = group_user
        exclude = ('author',)
        include = ('author_username',)

    def get_author_username(self, obj):
        return obj.get_username()
