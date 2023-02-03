from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('my-tasks', views.my_tasks, name="my-tasks"),
    path('create-tasks/', views.create_tasks, name="create-task"),
    path('update-task/<int:task_id>/', views.update_task, name="update-task"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]
