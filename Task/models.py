from django.db import models
from User.models import Team, User


class Task(models.Model):
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CreatedTasks')
    teams = models.ManyToManyField(Team, related_name='TeamTasks')
    title = models.CharField(max_length=20)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

class SubTask(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='TeamSubTasks')
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='SubTasks')
    