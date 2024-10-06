from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from applications.contacts.models import Contact
from applications.tags.models import Tag


User = get_user_model()


class ContactTestCases(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test-owner@example.com', password='test-password123',
                                             first_name='owner', last_name='owner')
        self.contact1 = Contact.objects.create(owner=self.user, name='Test contact 1', rating=4,
                                               phone_number='+1 234 5678 910')
        self.contact2 = Contact.objects.create(owner=self.user, name='Test contact 2', rating=5,
                                               phone_number='+9 876 543 210')
        self.contact3 = Contact.objects.create(owner=self.user, name='Test contact 3', rating=5,
                                               phone_number='+777 777 777 7')
        self.contact4 = Contact.objects.create(owner=self.user, name='Test contact 4', rating=3,
                                               phone_number='+11111111111111111')
        self.tag1 = Tag.objects.create(owner=self.user, name='Test tag1')
        self.tag2 = Tag.objects.create(owner=self.user, name='Test tag2')
        self.tag1.contacts.add(self.contact1, self.contact2)
        self.tag2.contacts.add(self.contact2, self.contact3)
        self.client.force_authenticate(self.user)

    def test_tag_list(self):
        url = reverse('tag-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('id'), self.tag2.id)

    def test_filter_contacts_by_single_tag_id(self):
        url = reverse('contact-list')
        url += f'?tags={self.tag1.id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        data = response.data['results']
        self.assertEqual([data[0].get('id'), data[1].get('id'), ], [self.contact2.id, self.contact1.id, ])

    def test_filter_contacts_by_multiple_tag_ids(self):
        url = reverse('contact-list')
        url += f'?tags={self.tag1.id},{self.tag2.id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        data = response.data['results']
        self.assertEqual([data[0].get('id'), data[1].get('id'), data[2].get('id')],
                         [self.contact3.id, self.contact2.id, self.contact1.id, ])

    def test_filter_contacts_by_invalid_query_string(self):
        url = reverse('contact-list')
        invalid_string = '!@#$%^&*()'
        url += f'?tags={invalid_string}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('tags'), ['Enter a number.', ])
