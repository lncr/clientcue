from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from applications.teams.models import Team, Role, Agent
from applications.tasks.models import Task


User = get_user_model()


class ContactTestCases(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='test-admin@example.com', password='test-password123',
                                                        first_name='admin', last_name='admin')
        self.agent_user = User.objects.create_user(email='test-agent@example.com', password='test-password123',
                                                   first_name='agent', last_name='agent')
        self.agent_user1 = User.objects.create_user(email='test-agent1@example.com', password='test-password123',
                                                    first_name='agent1', last_name='agent1')
        self.agent_user2 = User.objects.create_user(email='test-agent2@example.com', password='test-password123',
                                                    first_name='agent2', last_name='agent2')
        self.admin_team = Team.objects.create(owner=self.admin_user, name='Admin Team')
        self.team1 = Team.objects.create(owner=self.agent_user, name='Team1')
        self.team2 = Team.objects.create(owner=self.agent_user1, name='Team2')
        self.role1 = Role.objects.create(name='Role1', team=self.team1)
        self.role2 = Role.objects.create(name='Role2', team=self.team1)
        self.role3 = Role.objects.create(name='Role3', team=self.team2)
        self.agent1 = Agent.objects.create(user=self.agent_user)
        self.agent2 = Agent.objects.create(user=self.agent_user1)
        self.agent3 = Agent.objects.create(user=self.agent_user2)
        self.agent1.roles.add(self.role1)
        self.agent2.roles.add(self.role2)
        self.agent3.roles.add(self.role3)
        deadline = date.today() + timedelta(days=1)
        self.task1 = Task.objects.create(assigned_to=self.agent1, deadline=deadline, description='Test')
        self.task2 = Task.objects.create(assigned_to=self.agent1, deadline=deadline, description='Test')
        self.task3 = Task.objects.create(assigned_to=self.agent2, deadline=deadline, description='Test')
        self.task4 = Task.objects.create(assigned_to=self.agent2, deadline=deadline, description='Test')
        self.task5 = Task.objects.create(assigned_to=self.agent3, deadline=deadline, description='Test')
        self.task6 = Task.objects.create(assigned_to=self.agent3, deadline=deadline, description='Test')

    def test_list_of_tasks_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)

    def test_list_of_tasks_by_different_agent(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_of_tasks_by_team_id(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('task-list') + f'?team={self.team1.id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_list_of_assigned_tasks_by_agent(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('task-list') + 'assigned/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('id'), self.task1.id)

    def test_creating_of_task(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('task-list')
        deadline = date.today() + timedelta(days=5)
        data = {
            'assigned_to': self.agent1.id,
            'description': 'test description',
            'deadline': deadline
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_creating_of_task_with_invalid_deadline(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('task-list')
        deadline = date.today() - timedelta(days=1)
        data = {
            'assigned_to': self.agent1.id,
            'description': 'test description',
            'deadline': date.strftime(deadline, '%Y-%m-%d')
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
