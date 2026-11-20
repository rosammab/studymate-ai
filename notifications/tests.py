
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Notification


class NotificationAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="TestPassword123!"
        )

        self.other_user = User.objects.create_user(
            username="student2",
            password="TestPassword123!"
        )

        token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )

        self.notification = Notification.objects.create(
            user=self.user,
            title="Study reminder",
            message="Complete your Python revision.",
            notification_type="reminder"
        )

    def test_list_notifications(self):
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, 200)

    def test_mark_notification_as_read(self):
        response = self.client.post(
            f"/api/notifications/{self.notification.id}/read/"
        )

        self.assertEqual(response.status_code, 200)

        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_other_user_cannot_access_notification(self):
        response = self.client.get(
            f"/api/notifications/{self.notification.id}/"
        )
        self.assertEqual(response.status_code, 404)

    def test_unread_count(self):
        response = self.client.get(
            "/api/notifications/unread-count/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unread_count"], 1)
