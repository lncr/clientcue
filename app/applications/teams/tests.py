from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from applications.teams.models import Agent, Role, Team


User = get_user_model()


class TeamTestCases(APITestCase):

    def setUp(self):
        self.owner_user = User.objects.create_user(email='test-owner@example.com', password='test-password123',
                                                   first_name='owner', last_name='owner')
        self.agent_user1 = User.objects.create_user(email='test-agent1-user@example.com', password='password123',
                                                   first_name='agent', last_name='agent')
        self.agent_user2 = User.objects.create_user(email='test-agent2-user@example.com', password='password123',
                                                    first_name='agent', last_name='agent')
        self.agent1 = Agent.objects.create(user=self.agent_user1)
        self.agent2 = Agent.objects.create(user=self.agent_user2)
        self.blank_team = Team.objects.create(name='BlankTeam')
        self.team1 = Team.objects.create(name='Team1', owner=self.owner_user)
        self.team2 = Team.objects.create(name='Team2', owner=self.owner_user)
        self.role1 = Role.objects.create(name='Role1', team=self.team1)
        self.role2 = Role.objects.create(name='Role2', team=self.team1)
        self.role3 = Role.objects.create(name='Role3', team=self.team2)
        self.role4 = Role.objects.create(name='Role4', team=self.team2)
        self.role5 = Role.objects.create(name='Role5', team=self.blank_team)
        self.agent1.roles.add(self.role1)
        self.agent2.roles.add(self.role3)
        self.client.force_authenticate(self.owner_user)

    def test_team_list(self):
        url = reverse('team-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        data = [
            {
                'id': self.team2.id,
                'name': self.team2.name,
                'roles': [self.role3.id, self.role4.id, ],
                'participants_count': 1,
            },
            {
                'id': self.team1.id,
                'name': self.team1.name,
                'roles': [self.role1.id, self.role2.id, ],
                'participants_count': 1,
            },
        ]
        self.assertEqual(response.json().get('results'), data)

    def test_team_create(self):
        url = reverse('team-list')
        data = {'name': 'New test team', }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('name'), 'New test team')

    def test_team_list_by_agent(self):
        url = reverse('team-list')
        self.client.force_authenticate(self.agent_user1)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_role_create(self):
        url = reverse('role-list')
        data = {'team': self.team1.id, 'name': 'New test role', }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('name'), 'New test role')

    def test_role_list_by_owner(self):
        url = reverse('role-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 4)
        data = [
            {'id': self.role4.id, 'team': self.team2.id, 'name': 'Role4', 'agents': [], },
            {'id': self.role3.id, 'team': self.team2.id, 'name': 'Role3', 'agents': [self.agent2.id, ], },
            {'id': self.role2.id, 'team': self.team1.id, 'name': 'Role2', 'agents': [], },
            {'id': self.role1.id, 'team': self.team1.id, 'name': 'Role1', 'agents': [self.agent1.id, ], },
        ]
        self.assertEqual(response.data['results'], data)

    def test_role_list_by_agent(self):
        url = reverse('role-list')
        self.client.force_authenticate(self.agent_user1)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        data = [
            {'id': self.role2.id, 'team': self.team1.id, 'name': 'Role2', 'agents': [], },
            {'id': self.role1.id, 'team': self.team1.id, 'name': 'Role1', 'agents': [self.agent1.id, ], },
            ]
        self.assertEqual(response.data['results'], data)

    def test_agents_list_by_owner(self):
        url = reverse('agent-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        data = [
            {
                'id': self.agent2.id,
                'first_name': self.agent2.user.first_name,
                'last_name': self.agent2.user.last_name,
                'email': self.agent2.user.email,
                'email_confirmed': self.agent2.email_confirmed,
                'phone_number': self.agent2.phone_number,
                'phone_number_confirmed': self.agent2.phone_number_confirmed,
                'roles': [self.role3.id, ],
                'user': self.agent2.user.id,
            },
            {
                'id': self.agent1.id,
                'first_name': self.agent1.user.first_name,
                'last_name': self.agent1.user.last_name,
                'email': self.agent1.user.email,
                'email_confirmed': self.agent1.email_confirmed,
                'phone_number': self.agent1.phone_number,
                'phone_number_confirmed': self.agent1.phone_number_confirmed,
                'roles': [self.role1.id, ],
                'user': self.agent1.user.id,
            },
        ]
        self.assertEqual(response.data['results'], data)

    def test_agents_list_by_agent(self):
        url = reverse('agent-list')
        self.client.force_authenticate(self.agent_user1)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        data = [
            {
                'id': self.agent1.id,
                'first_name': self.agent1.user.first_name,
                'last_name': self.agent1.user.last_name,
                'email': self.agent1.user.email,
                'email_confirmed': self.agent1.email_confirmed,
                'phone_number': self.agent1.phone_number,
                'phone_number_confirmed': self.agent1.phone_number_confirmed,
                'roles': [self.role1.id, ],
                'user': self.agent1.user.id,
            },
        ]
        self.assertEqual(response.data['results'], data)
