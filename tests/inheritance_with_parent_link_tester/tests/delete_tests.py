from django.test import TestCase

from tests.inheritance_with_parent_link_tester.models import (Course, Video, Quiz, Unit)
from tests.inheritance_with_parent_link_tester.tests.helper import set_up_helper

class DeleteParentLinkTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_video(self):
        item = Video.objects.filter(pk=1).first()
        item.delete()

        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 2", 1, 3),
                           (1, "Video 3", 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_quiz(self):
        item = Quiz.objects.filter(pk=2).first()
        item.delete()

        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 2", 2, 4),
                           (1, "Quiz 3", 4, 6)]
        self.assertEqual(result, expected_result)

    def test_delete_unit(self):
        item = Unit.objects.filter(pk=1).first()
        item.delete()

        course = Course.objects.filter(pk=1).first()
        result = list(course.unit_set.values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 1", 0, 2),
                           (1, "Video 2", 1, 3),
                           (1, "Quiz 2", 2, 4),
                           (1, "Video 3", 3, 5),
                           (1, "Quiz 3", 4, 6)]
        self.assertEqual(result, expected_result)


