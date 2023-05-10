from django.urls import path
from .views import task_view_edit, task_list, task_create, comment_create, comment_detail, comment_edit, user_group_create, user_group_datail_edit

app_name = 'tasks'

urlpatterns = [
        path('<int:pk>/', task_view_edit.as_view()),
        path('create/', task_create.as_view()),
        path('usertasks/', task_list.as_view()),
        path('comment/create/', comment_create.as_view()),
        path('comment/detail/<int:pk>/', comment_detail.as_view()),
        path('comment/edit/<int:pk>/', comment_edit.as_view()),
        path('usergroup/create/', user_group_create.as_view()),
        path('usergroup/<int:pk>/', user_group_datail_edit.as_view()),
    ]