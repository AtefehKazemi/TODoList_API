from .models import task
from .serializers import task_serializer, task_create_serializer
from rest_framework import generics
from django.contrib.auth.models import User
from user_groups.models import group_user
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# used for viewing a task's details
# the user is able to view tasks that is author of or a member of one of their groupe
class task_view(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer

    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        user_groups = group_user.objects.filter(members=self.request.user.id)
        queryset = task.objects.filter(Q(id = pk) & (Q(author=self.request.user.id) | Q(task_groups__in = user_groups))).distinct()
        return queryset


# used for viewing a user's tasks list
# user may be task author or in one of its groups members
class task_list(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer

    # group objects that requested user is a member of, are filtered
    # task objects that user is the author of or in one of their groups, are filtered
    # retruns queryset
    def get_queryset(self):
        user_groups = group_user.objects.filter(members=self.request.user.id)
        queryset = task.objects.filter(Q(author=self.request.user.id) | Q(task_groups__in = user_groups)).distinct()
        return queryset


# used for creating a new task
class task_create(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = task_create_serializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)