from django.test import TestCase

from tests.ordered_table.models import HearthstoneRanking
from tests.ordered_table.tests.helper import set_up_helper


class ListInsertTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_insert_first(self):
        item_1_1 = HearthstoneRanking(name="new", rank=0)
        item_1_1.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 6), ("a", 1, 1, 1), ("a", 1, 2, 2), ("a", 1, 3, 3), ("a", 1, 4, 4), ("a", 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_second(self):
        item_1_1 = HearthstoneRanking(name="new")
        item_1_1.rank=1
        item_1_1.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 6), ("a", 1, 2, 2), ("a", 1, 3, 3), ("a", 1, 4, 4), ("a", 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_middle(self):
        item_1_1 = HearthstoneRanking(name="new", rank=2)
        item_1_1.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 6), ("a", 1, 3, 3), ("a", 1, 4, 4), ("a", 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_seccond_last(self):
        item_1_1 = HearthstoneRanking(name="new", rank=4)
        item_1_1.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 3), ("", 0, 3, 4), ("", 0, 4, 6), ("a", 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_last(self):
        item_1_1 = HearthstoneRanking(name="new", rank=5)
        item_1_1.save()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("updated_by", "order_changed_count", "rank", "id"))
        expected_result = [("", 0, 0, 1), ("", 0, 1, 2), ("", 0, 2, 3), ("", 0, 3, 4), ("", 0, 4, 5), ("", 0, 5, 6)]
        self.assertEqual(result, expected_result)

    """def test_insert_above_max(self):
        item_1_1 = HearthstoneRanking(name="new", rank=111)
        index_asserted = False  # Ubgly, is there a asseetException???
        try:
            item_1_1.save()
        except  IndexError:
            index_asserted = True

        self.assertTrue(index_asserted)"""


    def test_insert_far_below_min(self):
        item_1_1 = HearthstoneRanking(name="new", rank=-7)

        index_asserted = False # Ubgly, is there a asseetException???
        try:
            item_1_1.save()
        except  IndexError:
            index_asserted = True

        self.assertTrue(index_asserted)



