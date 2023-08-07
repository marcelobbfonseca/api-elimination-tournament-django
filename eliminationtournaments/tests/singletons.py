from django.test import TestCase
from unittest.mock import patch
from django.utils import timezone

from tournament_api.settings import TIME_ZONE
from eliminationtournaments.singletons import BGScheduler

class SingletonTest(TestCase):

    def setUp(self) -> None:
        pass

    def test_singleton_instance(self):
        instance1 = BGScheduler.get_instance()
        instance2 = BGScheduler.get_instance()
        self.assertIs(instance1, instance2, "Instances should be the same")

    def test_print_data(self):
        instance = BGScheduler.get_instance()
        with patch('builtins.print') as mock_print:
            instance.print_data()
            mock_print.assert_called_with(instance)

    def test_existing_bg_jobs(self):
        bg = BGScheduler.get_instance()
        now = timezone.now().timestamp()

        end_date = timezone.datetime.fromtimestamp(now + 10)

        bg.sched.add_job(lambda : print('Call me maybe'), 'date', run_date=end_date, timezone=TIME_ZONE)
        self.assertTrue(len(bg.sched.get_jobs()) >= 1)
