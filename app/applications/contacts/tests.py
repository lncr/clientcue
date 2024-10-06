from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from applications.contacts.models import Contact


User = get_user_model()


class ContactTestCases(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='test-admin@example.com', password='test-password123',
                                                        first_name='admin', last_name='admin')
        self.owner_user = User.objects.create_user(email='test-owner@example.com', password='test-password123',
                                                   first_name='owner', last_name='owner')
        self.ordinary_user = User.objects.create_user(email='test-user@example.com', password='test-password123',
                                                      first_name='user', last_name='user')
        self.contact1 = Contact.objects.create(owner=self.owner_user, name='Test contact 1', rating=4,
                                               phone_number='+1 234 5678 910')
        self.contact2 = Contact.objects.create(owner=self.owner_user, name='Test contact 2', rating=5,
                                               phone_number='+9 876 543 210')
        self.contact3 = Contact.objects.create(owner=self.admin_user, name='Test contact 3', rating=5,
                                               phone_number='+777 777 777 7')

    def test_list_retrieve_by_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, 200)

    def test_list_retrieve_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.status_code, 200)

    def test_list_retrieve_by_ordinary_user(self):
        self.client.force_authenticate(user=self.ordinary_user)
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.status_code, 200)

    def test_create_contact(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list')
        data = {'name': 'Test contact 4', 'phone_number': '+11111111111', 'rating': 5}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        created_contact = Contact.objects.last()
        self.assertEqual(created_contact.owner_id, self.owner_user.id)
        self.assertTrue(created_contact.name == 'Test contact 4')

    def test_create_contact_without_phone_number(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list')
        data = {'name': 'Test contact 5', 'rating': 5}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_contact_without_name(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list')
        data = {'phone_number': '+11111111111', 'rating': 5}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_contact_without_rating(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list')
        data = {'name': 'Test contact 6', 'phone_number': '+11111111111', }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_retrieve_certain_contact_by_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.data.get('id'), self.contact1.id)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_certain_contact_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.data.get('id'), self.contact1.id)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_certain_contact_by_ordinary_user(self):
        self.client.force_authenticate(user=self.ordinary_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_change_contact_by_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        data = {'rating': 2}
        response = self.client.patch(url, data=data, format='json')
        changed_contact = Contact.objects.get(id=self.contact1.id)
        self.assertEqual(changed_contact.rating, 2)
        self.assertEqual(response.status_code, 200)

    def test_change_contact_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        data = {'rating': 1}
        response = self.client.patch(url, data=data, format='json')
        changed_contact = Contact.objects.get(id=self.contact1.id)
        self.assertEqual(changed_contact.rating, 1)
        self.assertEqual(response.status_code, 200)

    def test_change_contact_by_ordinary_user(self):
        self.client.force_authenticate(user=self.ordinary_user)
        url = reverse('contact-detail', kwargs={'pk': self.contact1.id})
        data = {'rating': 5}
        response = self.client.patch(url, data=data, format='json')
        changed_contact = Contact.objects.get(id=self.contact1.id)
        self.assertEqual(changed_contact.rating, self.contact1.rating)
        self.assertEqual(response.status_code, 404)

    def test_filter_by_created_at_by_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        created_date = date.strftime(self.contact1.created_at, '%Y-%m-%d')
        url = reverse('contact-list') + f'?created_at={created_date}'
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0].get('id'), self.contact2.id)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_created_at_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        created_date = date.strftime(self.contact1.created_at, '%Y-%m-%d')
        url = reverse('contact-list') + f'?created_at={created_date}'
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0].get('id'), self.contact3.id)
        self.assertEqual(response.status_code, 200)

    def test_filter_with_invalid_qurystring(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('contact-list') + f'?created_at=test-string'
        response = self.client.get(url, format='json')
        self.assertEqual(response.json().get('created_at'), ['Enter a valid date.'])
        self.assertEqual(response.status_code, 400)
