from django.urls import path
from .views import user_group_create, user_group_datail_edit

app_name = 'group_user'

urlpatterns = [
        path('create/', user_group_create.as_view()),
        path('<int:pk>/', user_group_datail_edit.as_view()),
]