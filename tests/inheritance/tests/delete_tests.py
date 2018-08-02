from django.test import TestCase

from tests.inheritance.models import (Course, Video, Quiz, Unit)
from tests.inheritance.tests.helper import set_up_helper


class DeleteInheritTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_video(self):
        item = Video.objects.filter(pk=1).first()
        item.delete()

        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 2", 0, 3),
                           (1, "Video 3", 1, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_quiz(self):
        item = Quiz.objects.filter(pk=2).first()
        item.delete()

        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 2", 0, 4),
                           (1, "Quiz 3", 1, 6)]
        self.assertEqual(result, expected_result)



