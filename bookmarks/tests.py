from django.test import TestCase
from unittest.mock import patch
from bookmarks.models import Registered
from users.models import User
from events_available.models import Events_online
from django.utils import timezone
from freezegun import freeze_time
import datetime
import logging

logger = logging.getLogger(__name__)

class SendEventRemindersTestCase(TestCase):
    @patch('bookmarks.tasks.send_message_to_user')
    @freeze_time("2024-07-22 14:00:00")
    def test_send_event_reminders(self, mock_send_message_to_user):
        test_user = User.objects.create(username='testuser', telegram_id='1349308')

        start_time = timezone.now() + datetime.timedelta(days=1)
        date = start_time.date()
        time_start = start_time.time()
        time_end = (start_time + datetime.timedelta(hours=2)).time()

        event_online = Events_online.objects.create(
            name='Test Online Event',
            slug='test-online-event',
            date=date,
            time_start=time_start,
            time_end=time_end,
            description='Test description',
            platform='Zoom',
            link='http://testlink.com',
            category='Test Category',
            start_datetime=start_time  # добавляем start_datetime в событие
        )
        Registered.objects.create(
            user=test_user,
            online=event_online,
            start_datetime=start_time  # добавляем start_datetime
        )

        from bookmarks.tasks import send_event_reminders

        # Check reminders for 1 day
        with freeze_time("2024-07-23 14:00:00"):
            send_event_reminders()
            logger.info(f"Call count after 1 day reminder: {mock_send_message_to_user.call_count}")
            self.assertEqual(mock_send_message_to_user.call_count, 1)
            expected_message = f'Ваше событие "{event_online.name}" начнется через 1 day, 0:00:00.'
            mock_send_message_to_user.assert_called_with('1349308', expected_message)

        # Check reminders for 1 hour
        mock_send_message_to_user.reset_mock()
        with freeze_time("2024-07-24 13:00:00"):
            send_event_reminders()
            logger.info(f"Call count after 1 hour reminder: {mock_send_message_to_user.call_count}")
            self.assertEqual(mock_send_message_to_user.call_count, 1)
            expected_message = f'Ваше событие "{event_online.name}" начнется через 1:00:00.'
            mock_send_message_to_user.assert_called_with('1349308', expected_message)

        # Check reminders for 5 minutes
        mock_send_message_to_user.reset_mock()
        with freeze_time("2024-07-24 13:55:00"):
            send_event_reminders()
            logger.info(f"Call count after 5 minutes reminder: {mock_send_message_to_user.call_count}")
            self.assertEqual(mock_send_message_to_user.call_count, 1)
            expected_message = f'Ваше событие "{event_online.name}" начнется через 0:05:00.'
            mock_send_message_to_user.assert_called_with('1349308', expected_message)
