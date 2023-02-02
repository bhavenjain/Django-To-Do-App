import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tasks.models import Task
from django.contrib.auth.models import User
from tasks.serializers import TaskSerializer

# GET Routes

# Get all the tasks /tasks

@api_view(["GET"])
def get_all_tasks(request, *args, **kwargs):
    uid = request.GET['user_id']
    try:
        user_obj = User.objects.filter(pk = uid).first()
        instance = Task.objects.filter(author = user_obj).order_by('-deadline')
        all_tasks_list = []
        if instance:
            for task in instance:
                data = {}
                data = TaskSerializer(task).data
                all_tasks_list.append(data)
            return Response(all_tasks_list)
        else:
            return HttpResponse(status=404)

    except Exception as e:
      print(e)
    
# get a certain task
@api_view(["GET"])
def get_task(request, task_id, *args, **kwargs):
    instance = Task.objects.filter(pk=task_id).first()
    data = {}
    if instance:
        data = TaskSerializer(instance).data
    else:
        return HttpResponse(status=404)
    return Response()

# Post Routes

# Create new task
@api_view(["POST"])
def post_tasks(request, *args, **kwargs):
    instance = request.data
    user_id = request.GET.get('user_id')
    try:
        user_obj = User.objects.filter(pk=user_id).first()
        task_obj = Task.objects.create(
            title=instance['title'],
            content=instance['content'],
            deadline=instance['deadline'],
            author=user_obj
        )
        task_obj.save()
        return Response({'status': 200})
    except Exception as e:
        return Response({'status': 500})
    return Response({'status': 404})

# Update the completion status 
@api_view(["POST"])
def update_task(request, *args, **kwargs):
    task_id = request.GET.get('task_id')
    if task_id:
        try:
            task_obj = Task.objects.filter(pk = task_id).first()
            task_obj.completion_status = "Completed"
            task_obj.save()
        except Exception as e:
            return Response({'status': 500, 'message': e})
        

# Update the completion status 
@api_view(["DELETE"])
def delete_task(request, *args, **kwargs):
    task_id = request.GET.get('task_id')
    if task_id:
        try:
            task_obj = get_object_or_404(Task, pk=task_id)
            task_obj.delete()
        except Exception as e:
          print(e)