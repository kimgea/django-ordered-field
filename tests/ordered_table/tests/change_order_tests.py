from django.test import TestCase

from tests.ordered_table.models import HearthstoneRanking
from tests.ordered_table.tests.helper import set_up_helper

# Kind of duplicated, but not exactly :(


class ListChangeOrderTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_change_order_first_to_second(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        item.rank= 1
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 2), ("a", 1, 1, 1), ("", 0, 2, 3), ("", 0, 3, 4), ("", 0, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_first_to_middle(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        item.rank= 2
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 2), ("a", 1, 1, 3), ("a", 1, 2, 1), ("", 0, 3, 4), ("", 0, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_first_to_last(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        item.rank= 4
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 2), ("a", 1, 1, 3), ("a", 1, 2, 4), ("a", 1, 3, 5), ("a", 1, 4, 1)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_one_up(self):
        item = HearthstoneRanking.objects.filter(rank=2).first()
        item.rank= 1
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("a", 1, 1, 3), ("a", 1, 2, 2), ("", 0, 3, 4), ("", 0, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_one_down(self):
        item = HearthstoneRanking.objects.filter(rank=2).first()
        item.rank= 3
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("a", 1, 2, 4), ("a", 1, 3, 3), ("", 0, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_to_first(self):
        item = HearthstoneRanking.objects.filter(rank=2).first()
        item.rank= 0
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 3), ("a", 1, 1, 1), ("a", 1, 2, 2), ("", 0, 3, 4), ("", 0, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_to_last(self):
        item = HearthstoneRanking.objects.filter(rank=2).first()
        item.rank= 4
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("a", 1, 2, 4), ("a", 1, 3, 5), ("a", 1, 4, 3)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_second_last(self):
        """result = list(HearthstoneRanking.objects.all().order_by("rank").
                      values_list("rank", "id"))

        print(result)"""
        item = HearthstoneRanking.objects.filter(rank=4).first()
        item.rank= 3
        item.save()

        result = list(HearthstoneRanking.objects.all().order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 3), ("a", 1, 3, 5), ("a", 1, 4, 4)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_middle(self):
        item = HearthstoneRanking.objects.filter(rank=4).first()
        item.rank= 2
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("a", 1, 2, 5), ("a", 1, 3, 3), ("a", 1, 4, 4)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_first(self):
        item = HearthstoneRanking.objects.filter(rank=4).first()
        item.rank= 0
        item.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("a", 1, 0, 5), ("a", 1, 1, 1), ("a", 1, 2, 2), ("a", 1, 3, 3), ("a", 1, 4, 4)]
        self.assertEqual(result, expected_result)
