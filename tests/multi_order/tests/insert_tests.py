from django.test import TestCase

from tests.multi_order.models import List, Item
from tests.multi_order.tests.helper import set_up_helper


class InsertMultiOrderTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_insert_collection(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item(name="ssss", list=list2, order=0)
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 0, 0, 0, 1),
                           (1, 1, 0, 1, 0, 2),
                           (1, 2, 0, 2, 0, 3),
                           (2, 0, 0, 4, 0, 5),
                           (2, 1, 1, 3, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_insert_new_collection(self):
        list2 = List(name="list gggg")
        list2.save()
        item = Item(name="eeeewwww", list=list2, order=0)
        item.name = "ffafaf"
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 0, 0, 0, 1),
                           (1, 1, 0, 1, 0, 2),
                           (1, 2, 0, 2, 0, 3),
                           (2, 0, 0, 3, 0, 4),
                           (3, 0, 0, 4, 0, 5)]
        self.assertEqual(result, expected_result)
