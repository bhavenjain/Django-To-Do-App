from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    deadline = models.DateField()
    completion_status = models.CharField(max_length=20, default='Incomplete')
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title