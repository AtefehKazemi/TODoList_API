from django.urls import path
from .views import task_view, task_list, task_create

app_name = 'tasks'

urlpatterns = [
        path('<int:pk>/', task_view.as_view()),
        path('create/', task_create.as_view()),
        path('usertasks/', task_list.as_view()),
    ]