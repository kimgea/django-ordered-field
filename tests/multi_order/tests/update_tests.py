from django.test import TestCase

from tests.multi_order.models import List, Item
from tests.multi_order.tests.helper import set_up_helper


class ChangeMultiOrderTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_change_collection(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item.objects.filter(list=1, order=0).first()
        item.list = list2
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 1, 1, 0, 2), (1, 1, 1, 2, 0, 3), (2, 0, 0, 3, 0, 4), (2, 1, 0, 0, 0, 1)]
        self.assertEqual(result, expected_result)

    def test_change_order(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 1, 1, 0, 2), (1, 1, 1, 2, 0, 3), (1, 2, 1, 0, 0, 1), (2, 0, 0, 3, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_no_order_or_rank_change(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.name = "ffafaf"
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 0, 0, 0, 1), (1, 1, 0, 1, 0, 2), (1, 2, 0, 2, 0, 3), (2, 0, 0, 3, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_change_rank(self):
        item = Item.objects.filter(rank=0).first()
        item.rank = -1
        item.save()

        result = list(Item.objects.order_by("rank").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1, 2), (1, 2, 0, 1, 1, 3), (2, 0, 0, 2, 1, 4), (1, 0, 0, 3, 1, 1)]
        self.assertEqual(result, expected_result)
