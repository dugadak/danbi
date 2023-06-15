from django.db import models
from User.models import Team, User

class SubTask(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='TeamsubTasks')
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
class Task(models.Model):
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CreatedTasks')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='TeamTasks')
    title = models.CharField(max_length=20)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    SubTask = models.ForeignKey(SubTask, on_delete=models.CASCADE, related_name='MainTasks')
    

    