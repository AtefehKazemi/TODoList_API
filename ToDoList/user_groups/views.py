from django.shortcuts import render
from .models import group_user
from .serializers import group_user_serializer
from rest_framework import generics


class user_group_create(generics.CreateAPIView):
    serializer_class = group_user_serializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class user_group_datail_edit(generics.RetrieveUpdateDestroyAPIView):
    queryset = group_user.objects.all()
    serializer_class = group_user_serializer