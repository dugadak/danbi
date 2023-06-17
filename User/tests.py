from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from User.models import User, Team


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='단비')
        self.team2 = Team.objects.create(name='다래')
        self.team3 = Team.objects.create(name='철로')
        self.team4 = Team.objects.create(name='수피')
        self.team5 = Team.objects.create(name='기타팀')
        self.user = User.objects.create(username='이병준', team_id='단비')
        self.user.set_password('testpassword')
        self.user.save()
        self.signup_url = reverse('user-signup')
        self.signin_url = reverse('user-signin')
        self.refresh_token_url = reverse('user-refresh-access-token')
    
    def test_signup(self):
        data = {
            'username': 'bang',
            'team': '단비',
            'password': 'qangqang1234'
        }
        response = self.client.post(self.signup_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('refresh_token', response.data)

        
    def test_signin(self):
        data = {
            'username': '이병준',
            'password': 'testpassword'
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh_token', response.data)

        
    def test_refresh_access_token(self):
        signin_data = {
            'username': '이병준',
            'password': 'testpassword'
        }
        signin_response = self.client.post(self.signin_url, signin_data, format='json')
        
        refresh_token = signin_response.data.get('refresh_token') # 유효한 refresh token을 지정
        data = {
            'refresh_token': refresh_token
        }
        response = self.client.post(self.refresh_token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

