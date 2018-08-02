from django.test import TestCase

from tests.inheritance_with_parent_link_tester.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.inheritance_with_parent_link_tester.tests.helper import set_up_helper_two

class DeleteParentLinkTwoTest(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_delete_video(self):
        item = VideoTwo.objects.filter(pk=1).first()
        item.delete()

        result = list(VideoTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Video 2", 1, 3),
                           ("Video 3", 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_quiz(self):
        item = QuizTwo.objects.filter(pk=2).first()
        item.delete()

        result = list(QuizTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Quiz 2", 2, 4),
                           ("Quiz 3", 4, 6)]
        self.assertEqual(result, expected_result)

    def test_delete_unit(self):
        item = UnitTwo.objects.filter(pk=1).first()
        item.delete()

        result = list(UnitTwo.objects.all().values_list("name", "position", "id"))
        expected_result = [("Quiz 1", 0, 2),
                           ("Video 2", 1, 3),
                           ("Quiz 2", 2, 4),
                           ("Video 3", 3, 5),
                           ("Quiz 3", 4, 6)]
        self.assertEqual(result, expected_result)


