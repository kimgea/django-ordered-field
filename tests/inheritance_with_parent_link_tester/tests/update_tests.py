from django.test import TestCase


from tests.inheritance_with_parent_link_tester.models import (Course, Video, Quiz, Unit)
from tests.inheritance_with_parent_link_tester.tests.helper import set_up_helper


class ChangeParentLinkTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_video_update(self):
        video = Video.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 2", 1, 3),
                           (1, "Video 3", 3, 5),
                           (1, "Video 1", 5, 1)]
        self.assertEqual(result, expected_result)

    def test_quiz_update(self):
        quiz = Quiz.objects.filter(pk=2).first()
        quiz.position = -1
        quiz.save()
        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 2", 2, 4),
                           (1, "Quiz 3", 4, 6),
                           (1, "Quiz 1", 5, 2)]
        self.assertEqual(result, expected_result)

    def test_all_update(self):
        unit = Unit.objects.filter(pk=1).first()
        unit.position = 6
        unit.save()
        course = Course.objects.filter(pk=1).first()
        result = list(course.unit_set.order_by("position").values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 1", 0, 2),
                           (1, "Video 2", 1, 3),
                           (1, "Quiz 2", 2, 4),
                           (1, "Video 3", 3, 5),
                           (1, "Quiz 3", 4, 6),
                           (1, "Video 1", 5, 1)]
        self.assertEqual(result, expected_result)
