from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'content',
            'deadline',
            'author',
            'completion_status',
            'created_at'
        ]