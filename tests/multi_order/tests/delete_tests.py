from django.test import TestCase

from tests.multi_order.models import List, Item
from tests.multi_order.tests.helper import set_up_helper


class DeleteMultiOrderTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_from_collection_with_multiple(self):
        item = Item.objects.filter(list_id=1, order=0).first()
        item.delete()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 1, 0, 1, 2),
                           (1, 1, 1, 1, 1, 3),
                           (2, 0, 0, 2, 1, 4)]
        self.assertEqual(result, expected_result)

    def test_delete_from_collection_with_one(self):
        item = Item.objects.filter(list_id=2).first()
        item.delete()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "order_changed_count", "rank", "rank_changed_count", "id"))
        expected_result = [(1, 0, 0, 0, 0, 1),
                           (1, 1, 0, 1, 0, 2),
                           (1, 2, 0, 2, 0, 3)]
        self.assertEqual(result, expected_result)





