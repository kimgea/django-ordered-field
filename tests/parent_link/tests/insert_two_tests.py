from django.test import TestCase

from tests.parent_link.models import (UnitTwo, VideoTwo, QuizTwo)
from tests.parent_link.tests.helper import set_up_helper_two


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

    """def test_insert_same_list_only(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item(name="ssss", list=list2, sub_coll=999)
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (1, 2, 0, 0, 3),
                           (2, 1, 0, 0, 4),
                           (2, 999, 0, 0, 5)]
        self.assertEqual(result, expected_result)"""


