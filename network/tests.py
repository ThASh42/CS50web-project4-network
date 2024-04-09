from django.test import TestCase
from django.urls import reverse
from .models import User

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
