from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from Task.models import Task, SubTask
from Task.serializers import TaskSerializer, SubTaskSerializer
from User.models import Team
from django.db.models import Q


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        task_data = request.data.get('task', {})
        subtask_data = request.data.get('subtask', [])
        task_teams = task_data.get('teams', [])
        # Task의 팀과 SubTask의 팀 모두 합쳐서 존재여부 체킹
        team_names = list(set(task_teams + subtask_data))
        task_data["create_user"] = request.user.id
        
        
        valid_teams = Team.objects.filter(name__in=team_names)
        # 존재하지 않는 팀을 요청할 경우 에러 반환
        if len(valid_teams) != len(team_names):
            return Response({'error': '잘못된 팀이 포함되어 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        # 실질적인 DB Write
        self.perform_create(serializer, subtask_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self,serializer, subtask_data):
        task = serializer.save()
        # SubTask 생성
        sub_tasks = []
        for subtask_title in subtask_data:
            sub_task = SubTask(team_id=subtask_title, task=task)
            sub_tasks.append(sub_task)
        if sub_tasks:
            SubTask.objects.bulk_create(sub_tasks)
    
    
    
    def list(self, request, *args, **kwargs):
        user_team = request.user.team
        # Teak 또는 SubTask가 요청자의 팀에 할당된 경우의 Task를 필터링 후 중복제거
        queryset = Task.objects.filter(Q(teams=user_team) | Q(SubTasks__team=user_team)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'Tasks': serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.create_user != request.user:
            return Response({'error': '작성자 이외에 수정이 불가합니다.'}, status=status.HTTP_403_FORBIDDEN)

        
        task_data = request.data.get('task', {})
        subtask_teams_data = request.data.get('subtask', [])

        # task 수정
        serializer = self.get_serializer(task, data=task_data, partial=True)
        serializer.is_valid(raise_exception=True)

        
        # task에 이미 존재하는 subtasks 불러오기
        existing_subtasks = task.SubTasks.all()

        # 요청한 subtask의 team이 기존에 존재하지 않는다면 subtask 삭제
        subtask_team_list = []
        for subtask in existing_subtasks:
            if subtask.is_complete == True:
                continue
            if not subtask.team.name in subtask_teams_data:
                subtask.delete()
            subtask_team_list.append(subtask.team)
        
        # 요청한 subtask의 팀이 subtask에 존재하지 않는 경우 subtask 생성
        for subtask_team in subtask_teams_data:
            if not subtask_team in subtask_team_list:
                SubTask.objects.create(task=task, team_id=subtask_team)
        
        # 실질적인 DB Write, SubTask가 모두 완료 되었는지 체킹
        self.perform_update(serializer)
        
        return Response(serializer.data)


    def perform_update(self, serializer):
        task = serializer.save()
        subtask = task.SubTasks
        # Task에 해당되는 SubTask가 모두 완료되었다면 Task도 완료처리
        if not subtask.filter(is_complete=False).exists():
            task.is_complete = True
            task.save()
    
class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        SubTaskTeam = request.data.get('team')
        Exist_team = list(Team.objects.values_list('name', flat=True))
        if not SubTaskTeam in Exist_team:
            return Response({'error': 'SubTask를 지정할 수 없는 팀 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        subtask = self.get_object()
        user_team = request.user.team.name
        # 소속된 팀 것이 아닌 SubTask는 완료처리 불가
        if not subtask.team.name == user_team:
            return Response({'error': 'SubTask 완료처리는 소속된 팀만 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_complete = request.data.get('is_complete')
        # is not None을 이용하여 False여도 변경
        if is_complete is None:
            return Response({'error' : '변경할 업무처리 상태가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 시리얼라이저를 거쳐 is_complete 업데이트
        serializer = self.get_serializer(subtask, data={'is_complete': is_complete}, partial=True)
        serializer.is_valid(raise_exception=True)

        # 실질적인 DB Write, SubTask가 모두 완료 되었는지 체킹
        self.perform_update(serializer)

        return Response(serializer.data)
    

    def perform_update(self, serializer):
        subtask = serializer.save()
        task = subtask.task
        # Task에 해당되는 SubTask가 모두 완료되었다면 Task도 완료처리
        if not task.SubTasks.filter(is_complete=False).exists():
            task.is_complete = True
            task.save()
