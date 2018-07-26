from django.test import TestCase

from tests.multi_collection.models import List, Item
from tests.multi_collection.tests.helper import set_up_helper


class InsertMultiCollectionTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_insert_same_list_only(self):
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
        self.assertEqual(result, expected_result)

    def test_insert_same_sub_coll_only(self):
        list2 = List(name="list aaaaa")
        list2.save()
        item = Item(name="ssss", list=list2, sub_coll=1)
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (1, 2, 0, 0, 3),
                           (2, 1, 0, 0, 4),
                           (3, 1, 0, 0, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_same_collection(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item(name="ssss", list=list2, sub_coll=1, order=0)
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (1, 2, 0, 0, 3),
                           (2, 1, 0, 0, 5),
                           (2, 1, 1, 1, 4)]
        self.assertEqual(result, expected_result)

    def test_all_new(self):
        list2 = List(name="list gggg")
        list2.save()
        item = Item(name="eeeewwww", list=list2, sub_coll=11, order=0)
        item.name = "ffafaf"
        item.save()

        result = list(Item.objects.order_by("list", "sub_coll", "order").
                      values_list("list", "sub_coll", "order", "order_changed_count", "id"))
        expected_result = [(1, 1, 0, 0, 1),
                           (1, 1, 1, 0, 2),
                           (1, 2, 0, 0, 3),
                           (2, 1, 0, 0, 4),
                           (3, 11, 0, 0, 5)]
        self.assertEqual(result, expected_result)
