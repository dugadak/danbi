from rest_framework import serializers
from Task.models import SubTask, Task

class SubTaskSerializer(serializers.ModelSerializer):
    completed_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    modified_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    class Meta:
        model = SubTask
        fields = '__all__'



class TaskSerializer(serializers.ModelSerializer):
    SubTasks = SubTaskSerializer(many=True, read_only=True)
    completed_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    modified_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    class Meta:
        model = Task
        fields = '__all__'