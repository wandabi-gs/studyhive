from django.test import TestCase
from django.urls import reverse
from user.models import CustomUser
from user.views import Login

class TestUser(TestCase):
    def test_user_creation(self):
        self.user = CustomUser.objects.create_user(
            username = "Test User",
            email = "testuser@email.com",
            password = "testpassword"
        )

class LoginTests(TestCase):
    def test_view_rendering(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response)