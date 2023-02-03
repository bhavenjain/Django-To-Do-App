from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
import json
from django.views.decorators.cache import cache_control

# from .models import Task

url = settings.ENDPOINT_URL

# Home Route


def home(request):
    if request.user.is_authenticated:
        return redirect('/my-tasks')
    return render(request, 'tasks/home.html', {'title': "Home"})

# Create tasks


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def create_tasks(request):
    if request.method == 'POST':
        user_obj = User.objects.filter(pk=request.user.id).first()
        data = request.POST
        title = data.get('title')
        content = data.get('content').strip()
        deadline = data.get('deadline')
        if title and content and deadline:
            endpoint = url + 'tasks/create_task/'
            data = {
                'title': title,
                'deadline': deadline,
                'content': content,
            }
            res = requests.post(
                endpoint, params={"user_id": user_obj.id}, json=data)

            if json.loads(res.text)['status'] == 200:
                # messages.success(request, "New task has been added")
                return redirect('/my-tasks')
            else:
                messages.error(request, "Task was not added. Please try again")
                return redirect('/create-tasks')

    return render(request, 'tasks/create_task.html')

# Tasks functions


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def my_tasks(request):
    # Update
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id and request.POST.get('Mark'):
            try:
                endpoint = url+'tasks/update/'
                res = requests.post(endpoint, params={'task_id': task_id})
                print(res)
            except Exception as e:
                print(e)

        if task_id and request.POST.get('update'):
            return redirect(f'/update-task/{task_id}')

        # Delete tasks
        if request.POST.get('Delete'):
            try:
                endpoint = url + 'tasks/delete/'
                res = requests.delete(endpoint, params={'task_id': task_id})
                print(res)
            except Exception as e:
                print(e)

    data = {}
    try:
        endpoint = url+'tasks'
        res = requests.get(endpoint, params={'user_id': request.user.id})
        data = json.loads(res.text)
    except Exception as e:
        print(e)
    return render(request, "tasks/tasks.html", {'tasks': data})

# Tasks functions


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def update_task(request, task_id):
    data = {}
    try:
        endpoint = url + f'tasks/{task_id}'
        task_obj = requests.get(endpoint)
        data = json.loads(task_obj.text)
    except Exception as e:
        print(e)
    
    if request.method == "POST":
        updated_data = request.POST
        task_id = updated_data.get('id')
        title = updated_data.get('title')
        content = updated_data.get('content').strip()
        deadline = updated_data.get('deadline') 
        try:
            endpoint = url + 'tasks/update-task/'
            res = requests.post(endpoint, params = {'task_id': task_id}, json={"title": title, 'content': content, 'deadline': deadline})
            res = json.loads(res.text)
            if res['status'] == 200:
                return redirect('/my-tasks')
        except Exception as e:
          print(e)
        
    return render(request, 'tasks/update.html', {'data': data})
