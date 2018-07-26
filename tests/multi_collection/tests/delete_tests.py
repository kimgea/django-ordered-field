from django.test import TestCase

from tests.multi_collection.models import List, Item
from tests.multi_collection.tests.helper import set_up_helper


class DeleteMultiCollectionTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_from_collection_with_multiple(self):
        list2 = List.objects.filter(pk=1).first()
        item = Item.objects.filter(list=list2, order=0, sub_coll=1).first()
        item.delete()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 1, 2),
                           (1, 2, 0, 0, 3),
                           (2, 1, 0, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_delete_from_collection_with_one_but_part_multiple_in_list(self):
        list2 = List.objects.filter(pk=1).first()
        item = Item.objects.filter(list_id=1, order=0, sub_coll=2).first()
        item.delete()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (2, 1, 0, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_delete_delete_when_only_one_in_list(self):
        item = Item.objects.filter(list_id=2, order=0, sub_coll=1).first()
        item.delete()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (1, 2, 0, 0, 3)]
        self.assertEqual(result, expected_result)


