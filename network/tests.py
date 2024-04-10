from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.messages import get_messages, constants

# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Make the user log in
        self.client.login(username='testuser', password='testpassword')
    
    def test_create_post_POST(self):
        # Post a new post
        response = self.client.post(reverse('create_post'), {'new-post-content-textarea': 'HI!'})
        
        self.assertEqual(response.status_code, 302)
    
    def test_create_post_POST_no_data(self):
        response = self.client.post(reverse('create_post'), {'new-post-content-textarea': ''})

        self.assertEqual(response.status_code, 302)

        # Assert that there is an error message
        message_found = False
        messages = get_messages(response.wsgi_request)
        for message in messages:
            if message.message == "Post cannot be empty" and 'error' in message.tags:
                message_found = True
                break
        self.assertTrue(message_found)
