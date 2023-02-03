from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_tasks),
    path('create_task/', views.post_tasks),
    path('<int:task_id>/', views.get_task),
    path('update/', views.update_task),
    path('update-task/', views.updated_tasks),
    path('delete/', views.delete_task),   
]
