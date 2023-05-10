from rest_framework import serializers
from .models import group_user


class group_user_serializer(serializers.ModelSerializer):
    creator_username = serializers.SerializerMethodField()

    class Meta:
        model = group_user
        fields = '__all__'
        read_only = ('creator',)
        include = ('creator_username',)

    def get_creator_username(self, obj):
        return obj.get_username()
