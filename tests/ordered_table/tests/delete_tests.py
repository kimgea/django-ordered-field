from django.test import TestCase

from tests.ordered_table.models import HearthstoneRanking
from tests.ordered_table.tests.helper import set_up_helper


class ListDeleteTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_first(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 2), ("a", 1, 1, 3), ("a", 1, 2, 4), ("a", 1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_second(self):
        item = HearthstoneRanking.objects.filter(rank=1).first()
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("a", 1, 1, 3), ("a", 1, 2, 4), ("a", 1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_middle(self):
        item = HearthstoneRanking.objects.filter(rank=2).first()
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("a", 1, 2, 4), ("a", 1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_second_last(self):
        item = HearthstoneRanking.objects.filter(rank=3).first()
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 3), ("a", 1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_last(self):
        item = HearthstoneRanking.objects.filter(rank=4).first()
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 3), ("", 0, 3, 4)]
        self.assertEqual(result, expected_result)
