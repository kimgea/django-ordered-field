from django.test import TestCase


from tests.inheritance_with_parent_link_tester.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.inheritance_with_parent_link_tester.tests.helper import set_up_helper_two


class ChangeParentLinkTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_video_update(self):
        video = VideoTwo.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video 2", 1, 3),
                           ("Video 3", 3, 5),
                           ("Video 1", 5, 1)]
        self.assertEqual(result, expected_result)

    def test_quiz_update(self):
        quiz = QuizTwo.objects.filter(pk=2).first()
        quiz.position = -1
        quiz.save()
        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz 2", 2, 4),
                           ("Quiz 3", 4, 6),
                           ("Quiz 1", 5, 2)]
        self.assertEqual(result, expected_result)

    def test_all_update(self):
        unit = UnitTwo.objects.filter(pk=1).first()
        unit.position = 6
        unit.save()
        result = list(UnitTwo.objects.all().order_by("position").values_list("name", "position", "id"))
        expected_result = [("Quiz 1", 0, 2),
                           ("Video 2", 1, 3),
                           ("Quiz 2", 2, 4),
                           ("Video 3", 3, 5),
                           ("Quiz 3", 4, 6),
                           ("Video 1", 5, 1)]
        self.assertEqual(result, expected_result)
