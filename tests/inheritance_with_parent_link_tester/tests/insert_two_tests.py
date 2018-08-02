from django.test import TestCase

from tests.inheritance_with_parent_link_tester.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.inheritance_with_parent_link_tester.tests.helper import set_up_helper_two


class InsertParentLinkTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_video_init(self):
        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video 1", 0, 1),
                           ("Video 2", 2, 3),
                           ("Video 3", 4, 5)]
        self.assertEqual(result, expected_result)

    def test_quiz_init(self):
        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz 1", 1, 2),
                           ("Quiz 2", 3, 4),
                           ("Quiz 3", 5, 6)]
        self.assertEqual(result, expected_result)

    def test_all_init(self):
        unit = UnitTwo.objects.all()
        result = list(unit.values_list("name", "position", "id"))
        expected_result = [("Video 1", 0, 1),
                           ("Quiz 1", 1, 2),
                           ("Video 2", 2, 3),
                           ("Quiz 2", 3, 4),
                           ("Video 3", 4, 5),
                           ("Quiz 3", 5, 6)]
        self.assertEqual(result, expected_result)

    def test_video_insert_front(self):
        video = VideoTwo(name="Video new", description="new", position=0)
        video.save()

        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video new", 0, 7),
                           ("Video 1", 1, 1),
                           ("Video 2", 3, 3),
                           ("Video 3", 5, 5)]
        self.assertEqual(result, expected_result)

    def test_quiz_insert_front(self):
        quiz = QuizTwo(name="Quiz new", questions="new", position=0)
        quiz.save()

        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz new", 0, 7),
                           ("Quiz 1", 2, 2),
                           ("Quiz 2", 4, 4),
                           ("Quiz 3", 6, 6)]
        self.assertEqual(result, expected_result)



