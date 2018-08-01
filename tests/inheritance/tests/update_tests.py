from django.test import TestCase

from tests.inheritance.models import (Course, Video, Quiz, Unit)
from tests.inheritance.tests.helper import set_up_helper


class ChangeInheritTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_video_update(self):
        video = Video.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 2", 0, 3),
                           (1, "Video 3", 1, 5),
                           (1, "Video 1", 2, 1)]
        self.assertEqual(result, expected_result)

    def test_quiz_update(self):
        quiz = Quiz.objects.filter(pk=2).first()
        quiz.position = -1
        quiz.save()
        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 2", 0, 4),
                           (1, "Quiz 3", 1, 6),
                           (1, "Quiz 1", 2, 2)]
        self.assertEqual(result, expected_result)

