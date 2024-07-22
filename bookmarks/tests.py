# bookmarks/tests.py

import datetime
from django.test import TestCase
from django.utils import timezone
from bookmarks.models import Registered
from bookmarks.tasks import send_event_reminders
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
from users.models import User, Department
from unittest.mock import patch
from freezegun import freeze_time

class SendEventRemindersTestCase(TestCase):
    def setUp(self):
        # Create test department and user
        self.department = Department.objects.create(department_id='test-dept', department_name='Test Department')
        self.user = User.objects.create(username='testuser', telegram_id='1349308', department=self.department)

        # Create test events
        now = timezone.now()
        self.event_online = Events_online.objects.create(
            name="Test Online Event",
            slug="test-online-event",
            date=now.date(),
            time_start=(now + datetime.timedelta(hours=25)).time(),
            time_end=(now + datetime.timedelta(hours=26)).time(),
            description="Description",
            speakers="Speakers",
            member="Members",
            tags="Tags",
            platform="Platform",
            link="https://example.com",
            events_admin="Admin"
        )
        self.event_online.start_datetime = now + datetime.timedelta(hours=25)
        self.event_online.save()

        self.event_offline = Events_offline.objects.create(
            name="Test Offline Event",
            slug="test-offline-event",
            date=now.date(),
            time_start=(now + datetime.timedelta(hours=1)).time(),
            time_end=(now + datetime.timedelta(hours=2)).time(),
            description="Description",
            speakers="Speakers",
            member="Members",
            tags="Tags",
            town="Town",
            street="Street",
            cabinet="Cabinet",
            link="https://example.com",
            events_admin="Admin"
        )
        self.event_offline.start_datetime = now + datetime.timedelta(hours=1)
        self.event_offline.save()

        Registered.objects.create(user=self.user, online=self.event_online)
        Registered.objects.create(user=self.user, offline=self.event_offline)

    @patch('users.telegram_utils.send_message_to_user')
    def test_send_event_reminders(self, mock_send_message_to_user):
        now = timezone.now()

        # Test for 24-hour reminder
        with freeze_time(now):
            send_event_reminders()
            self.assertEqual(mock_send_message_to_user.call_count, 1)
            call_args_24h = mock_send_message_to_user.call_args_list[0]
            self.assertIn("Напоминание: мероприятие 'Test Online Event' начинается скоро.", call_args_24h[0][1])

        # Test for 1-hour reminder
        with freeze_time(now + datetime.timedelta(hours=24)):
            send_event_reminders()
            self.assertEqual(mock_send_message_to_user.call_count, 2)
            call_args_1h = mock_send_message_to_user.call_args_list[1]
            self.assertIn("Напоминание: мероприятие 'Test Offline Event' начинается скоро.", call_args_1h[0][1])

        # Test for 5-minute reminder
        with freeze_time(now + datetime.timedelta(hours=1) - datetime.timedelta(minutes=5)):
            send_event_reminders()
            self.assertEqual(mock_send_message_to_user.call_count, 3)
            call_args_5m = mock_send_message_to_user.call_args_list[2]
            self.assertIn("Напоминание: мероприятие 'Test Offline Event' начинается скоро.", call_args_5m[0][1])
