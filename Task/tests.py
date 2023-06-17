import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Task.models import Task, SubTask
from User.models import User, Team

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='이병준', team_id='단비')
        self.user.set_password('testpassword')
        self.team1 = Team.objects.create(name='단비')
        self.team2 = Team.objects.create(name='다래')
        self.team3 = Team.objects.create(name='철로')
        self.team4 = Team.objects.create(name='수피')
        self.team5 = Team.objects.create(name='기타팀')
        self.task = Task.objects.create(title='Test Task', create_user=self.user)
        self.subtask1 = SubTask.objects.create(task=self.task, team=self.team1)
        self.subtask2 = SubTask.objects.create(task=self.task, team=self.team2)
    
    def test_create_task_with_valid_teams(self):
        url = reverse('task-list')
        data = {
            'task': {
                'title': 'New Task',
                'teams': [self.team1.name, self.team2.name, self.team3.name],
                'content' : 'testing',
                'create_user' : self.user.id
            },
            'subtask': []
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(SubTask.objects.count(), 2)
    
    def test_create_task_with_invalid_teams(self):
        url = reverse('task-list')
        data = {
            'task': {
                'title': 'New Task',
                'teams': [self.team1.name, self.team2.name, 'InvalidTeam'],
                'content' : 'testing',
                'create_user' : self.user.id
            },
            'subtask': []
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(SubTask.objects.count(), 2)
    
    def test_list_tasks_with_user_team(self):
        url = reverse('task-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['Tasks']), 1)
        self.assertEqual(response.data['Tasks'][0]['id'], self.task.id)
    
    def test_update_task_with_valid_teams(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'task': {
                'title': 'Updated Task',
                'teams': [self.team1.name, self.team2.name, self.team4.name]
            },
            'subtask': [self.team1.name, self.team2.name, self.team3.name]
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.teams.count(), 3)
        self.assertEqual(SubTask.objects.count(), 5)
    
    def test_update_task_with_completed_subtask(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'task': {
                'title': 'Updated Task',
                'teams': [self.team1.name, self.team2.name]
            },
            'subtask': [self.team1.name]
        }
        # Complete one subtask
        self.subtask1.is_complete = True
        self.subtask1.save()
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.teams.count(), 2)
        self.assertEqual(SubTask.objects.count(), 2)
    
    def test_update_task_by_non_creator_user(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'task': {
                'title': 'Updated Task',
                'teams': [self.team1.name, self.team2.name]
            },
            'subtask': []
        }
        non_creator_user = User.objects.create_user(username='none',team_id='단비', password='nonpassword')
        self.client.force_authenticate(non_creator_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Test Task')  # Title should not be updated
    
    def test_update_subtask_complete_status(self):
        url = reverse('subtask-detail', args=[self.subtask1.id])
        data = {
            'is_complete': True
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subtask1.refresh_from_db()
        self.assertEqual(self.subtask1.is_complete, True)
    
    def test_update_subtask_complete_status_by_non_team_member(self):
        url = reverse('subtask-detail', args=[self.subtask1.id])
        data = {
            'is_complete': True
        }
        non_member_user = User.objects.create_user(username='none',team_id=self.subtask2.team.name, password='nonpassword')
        self.client.force_authenticate(non_member_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.subtask1.refresh_from_db()
        self.assertEqual(self.subtask1.is_complete, False)  # Complete status should not be updated

