from .models import task, comment, group_user, notification
from .serializers import task_serializer_detail_edit, task_create_serializer, comment_serializer_view, comment_serializer_create_and_edit, group_user_serializer, notification_serializer
from rest_framework import generics
from django.contrib.auth.models import User
#from user_groups.models import group_user
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from functools import wraps


# cache function
def cache_response(key_prefix):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view_instance, request, *args, **kwargs):
            cache_key = f"{key_prefix}:{request.get_full_path()}"
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                print("*************from cache************")
                return cached_response
            print("*************no  cache************")
            response = view_func(view_instance, request, *args, **kwargs)
            cache.set(cache_key, response)
            return response
        return wrapper
    return decorator

# task views:

# used for viewing a task's details
# the user is able to view tasks that is author of or a member of one of their groupe
class task_view_edit(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer_detail_edit

    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        user_groups = group_user.objects.filter(members=self.request.user.id)
        queryset = task.objects.filter(Q(id = pk) & (Q(author=self.request.user.id) | Q(task_groups__in = user_groups))).distinct()
        return queryset


# used for viewing a user's tasks list
# user may be task author or in one of its groups members
class task_list(generics.ListAPIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    serializer_class = task_serializer_detail_edit

    # group objects that requested user is a member of, are filtered
    # task objects that user is the author of or in one of their groups, are filtered
    # retruns queryset
    def get_queryset(self):
        user_groups = group_user.objects.filter(members=self.request.user.id)
        queryset = task.objects.filter(Q(author=self.request.user.id) | Q(task_groups__in = user_groups)).distinct()
        return queryset
    
    '''
    def list(self, request, *args, **kwargs):
        key = 'task_list'
        data = cache.get(key)
        if not data:
            print("****************no cache*****************")
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(key, data, 300)
        else:
            print("*************from cache************")
        return Response(data)
    '''

    @cache_response(key_prefix='myapp:tasklistview')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# used for creating a new task
class task_create(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = task_create_serializer

    def perform_create(self, serializer):
        # we will send `author` in the `validated_data`
        serializer.save(author=self.request.user)


# Comment views:

# used for creating new comment
class comment_create(generics.CreateAPIView):
    serializer_class = comment_serializer_create_and_edit

    def perform_create(self, serializer):
        # we will send `author` in the `validated_data`
        serializer.save(author=self.request.user)


# used for viewing a comment's details
class comment_detail(generics.RetrieveAPIView):
    queryset = comment.objects.all()
    serializer_class = comment_serializer_view


# used for editing a comment
class comment_edit(generics.RetrieveUpdateDestroyAPIView):
    queryset = comment.objects.all()
    serializer_class = comment_serializer_create_and_edit


# group_user views:

class user_group_create(generics.CreateAPIView):
    serializer_class = group_user_serializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class user_group_datail_edit(generics.RetrieveUpdateDestroyAPIView):
    queryset = group_user.objects.all()
    serializer_class = group_user_serializer


# notification views:

# used for viewing a user's notifications
class user_notifications_list(generics.ListAPIView):
    serializer_class = notification_serializer
    
    def get_queryset(self):
        queryset = notification.objects.filter(receiver=self.request.user.id)
        return queryset


# used for viewing a notification details
# its id is given in url
class notification_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = notification.objects.all()
    serializer_class = notification_serializer