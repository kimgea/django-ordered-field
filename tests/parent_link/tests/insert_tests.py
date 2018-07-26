from django.test import TestCase

from tests.parent_link.models import (Course,Video,Quiz)
from tests.parent_link.tests.helper import set_up_helper


class InsertParentLinkTests(TestCase):
    def setUp(self):
        set_up_helper()


    def test_video_init(self):
        result = list(Video.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 1", 0, 1),
                           (1, "Video 2", 2, 3),
                           (1, "Video 3", 4, 5)]
        self.assertEqual(result, expected_result)

    def test_quiz_init(self):
        result = list(Quiz.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Quiz 1", 1, 2),
                           (1, "Quiz 2", 3, 4),
                           (1, "Quiz 3", 5, 6)]
        self.assertEqual(result, expected_result)

    def test_all_init(self):
        course = Course.objects.filter(pk=1).first()
        result = list(course.unit_set.values_list("course", "name", "position", "id"))
        expected_result = [(1, "Video 1", 0, 1),
                           (1, "Quiz 1", 1, 2),
                           (1, "Video 2", 2, 3),
                           (1, "Quiz 2", 3, 4),
                           (1, "Video 3", 4, 5),
                           (1, "Quiz 3", 5, 6)]
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


