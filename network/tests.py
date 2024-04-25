import json
from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.messages import get_messages

# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        # Create users
        self.main_user = User.objects.create_user(username='testuser', password='testpassword')
        self.second_user = User.objects.create_user(username='testseconduser', password='testsecondpassword')
        # Make the user log in
        self.client.login(username='testuser', password='testpassword')
    
    def test_create_post_POST(self):
        # Post a new post
        response = self.client.post(reverse('create_post'), {'add-new-post-form-textarea': 'HI!'})
        
        self.assertEqual(response.status_code, 302)
    
    def test_create_post_POST_no_data(self):
        response = self.client.post(reverse('create_post'), {'add-new-post-form-textarea': ''})

        self.assertEqual(response.status_code, 302)

        # Assert that there is an error message
        message_found = False
        messages = get_messages(response.wsgi_request)
        for message in messages:
            if message.message == "Post cannot be empty" and 'error' in message.tags:
                message_found = True
                break
        self.assertTrue(message_found)

    def test_is_following_view_post_and_delete(self):
        url = reverse('follow_unfollow', args=(self.second_user.username,))
        data = {
            'follower': self.main_user.username,
            'followed_user': self.second_user.username,
        }
        # make POST request
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 204)

        # make DELETE request
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 204)
