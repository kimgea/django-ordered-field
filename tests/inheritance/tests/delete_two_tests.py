from django.test import TestCase

from tests.inheritance.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.inheritance.tests.helper import set_up_helper_two


class DeleteInheritTwoTest(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_delete_video(self):
        item = VideoTwo.objects.filter(pk=1).first()
        item.delete()

        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video 2", 0, 3),
                           ("Video 3", 1, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_quiz(self):
        item = QuizTwo.objects.filter(pk=2).first()
        item.delete()

        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz 2", 0, 4),
                           ("Quiz 3", 1, 6)]
        self.assertEqual(result, expected_result)



