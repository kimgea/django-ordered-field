from django.test import TestCase

from tests.inheritance.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.inheritance.tests.helper import set_up_helper_two


class ChangeInheritTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_video_update(self):
        video = VideoTwo.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video 2", 0, 3),
                           ("Video 3", 1, 5),
                           ("Video 1", 2, 1)]
        self.assertEqual(result, expected_result)

    def test_quiz_update(self):
        quiz = QuizTwo.objects.filter(pk=2).first()
        quiz.position = -1
        quiz.save()
        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz 2", 0, 4),
                           ("Quiz 3", 1, 6),
                           ("Quiz 1", 2, 2)]
        self.assertEqual(result, expected_result)

