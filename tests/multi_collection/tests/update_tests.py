from django.test import TestCase

from tests.multi_collection.models import List, Item
from tests.multi_collection.tests.helper import set_up_helper


class ChangeMultiCollectionTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_change_list(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item.objects.filter(list=1, sub_coll=1, order=0).first()
        item.list = list2
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 1, 2), (1, 2, 0, 0, 3), (2, 1, 0, 0, 4), (2, 1, 1, 1, 1)]
        self.assertEqual(result, expected_result)

    def test_change_sub_coll(self):
        item = Item.objects.filter(list=1, sub_coll=1, order=0).first()
        item.sub_coll = 999
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 1, 2), (1, 2, 0, 0, 3), (1, 999, 0, 1, 1), (2, 1, 0, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_change_order(self):
        item = Item.objects.filter(list=1, sub_coll=1, order=0).first()
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 1, 2), (1, 1, 1, 1, 1), (1, 2, 0, 0, 3), (2, 1, 0, 0, 4)]
        self.assertEqual(result, expected_result)

    def test_no_order_change(self):
        item = Item.objects.filter(list=1, sub_coll=1, order=0).first()
        item.name = "ffafaf"
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1), (1, 1, 1, 0, 2), (1, 2, 0, 0, 3), (2, 1, 0, 0, 4)]
        self.assertEqual(result, expected_result)
