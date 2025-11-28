from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote

class PollTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.poll = Poll.objects.create(
            title="Test Poll",
            description="Test Description",
            expires_at=timezone.now() + timedelta(days=1)
        )
        self.choice1 = Choice.objects.create(poll=self.poll, text="Option 1")
        self.choice2 = Choice.objects.create(poll=self.poll, text="Option 2")
    
    def test_create_poll(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Poll',
            'description': 'New Description',
            'expires_at': (timezone.now() + timedelta(days=2)).isoformat(),
            'choices': [
                {'text': 'Choice 1'},
                {'text': 'Choice 2'}
            ]
        }
        response = self.client.post('/api/polls/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_active_polls(self):
        response = self.client.get('/api/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_vote_on_poll(self):
        data = {
            'choice_id': self.choice1.id,
            'voter_identifier': 'voter@example.com'
        }
        response = self.client.post(f'/api/polls/{self.poll.id}/vote/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
    
    def test_duplicate_vote_prevention(self):
        Vote.objects.create(
            poll=self.poll,
            choice=self.choice1,
            voter_identifier='voter@example.com'
        )
        data = {
            'choice_id': self.choice2.id,
            'voter_identifier': 'voter@example.com'
        }
        response = self.client.post(f'/api/polls/{self.poll.id}/vote/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_poll_results(self):
        Vote.objects.create(poll=self.poll, choice=self.choice1, voter_identifier='voter1@example.com')
        Vote.objects.create(poll=self.poll, choice=self.choice1, voter_identifier='voter2@example.com')
        Vote.objects.create(poll=self.poll, choice=self.choice2, voter_identifier='voter3@example.com')
        
        response = self.client.get(f'/api/polls/{self.poll.id}/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_votes'], 3)
    
    def test_close_poll(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/polls/{self.poll.id}/close/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.status, 'CLOSED')
    
    def test_vote_on_closed_poll(self):
        self.poll.status = 'CLOSED'
        self.poll.save()
        
        data = {
            'choice_id': self.choice1.id,
            'voter_identifier': 'voter@example.com'
        }
        response = self.client.post(f'/api/polls/{self.poll.id}/vote/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
