from django.test import TestCase

from tests.inheritance.models import (Course, Video, Quiz)
from tests.inheritance.tests.helper import set_up_helper


class InsertInheritTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_video_init(self):
        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 1", 0, 1),
                           (1, "Video 2", 1, 3),
                           (1, "Video 3", 2, 5)]
        self.assertEqual(result, expected_result)

    def test_quiz_init(self):
        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 1", 0, 2),
                           (1, "Quiz 2", 1, 4),
                           (1, "Quiz 3", 2, 6)]
        self.assertEqual(result, expected_result)

    def test_all_init(self):
        course = Course.objects.filter(pk=1).first()
        result = list(course.unit_set.values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 1", 0, 1),
                           (1, "Quiz 1", 0, 2),
                           (1, "Video 2", 1, 3),
                           (1, "Quiz 2", 1, 4),
                           (1, "Video 3", 2, 5),
                           (1, "Quiz 3", 2, 6)]
        self.assertEqual(result, expected_result)

    def test_video_insert_front(self):
        video = Video(course_id=1, name="Video new", description="new", position=0)
        video.save()

        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video new", 0, 7),
                           (1, "Video 1", 1, 1),
                           (1, "Video 2", 2, 3),
                           (1, "Video 3", 3, 5)]
        self.assertEqual(result, expected_result)

    def test_quiz_insert_front(self):
        quiz = Quiz(course_id=1, name="Quiz new", questions="new", position=0)
        quiz.save()

        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz new", 0, 7),
                           (1, "Quiz 1", 1, 2),
                           (1, "Quiz 2", 2, 4),
                           (1, "Quiz 3", 3, 6)]
        self.assertEqual(result, expected_result)



