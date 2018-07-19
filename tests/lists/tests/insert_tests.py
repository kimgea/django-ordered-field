from django.test import TestCase

from tests.lists.models import List, Item
from tests.lists.tests.helper import set_up_helper


class ListInsertTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_insert_first(self):
        list1 = List.objects.filter(pk=1).first()
        item_1_1 = Item(name="new", list=list1, order=0)
        item_1_1.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 7), ("a", 1, 1, 1, 1), ("a", 1, 1, 2, 2), ("a", 1, 1, 3, 3), ("a", 1, 1, 4, 4), ("a", 1, 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_second(self):
        list1 = List.objects.filter(pk=1).first()
        item_1_1 = Item(name="new", list=list1, order=1)
        item_1_1.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 7), ("a", 1, 1, 2, 2), ("a", 1, 1, 3, 3), ("a", 1, 1, 4, 4), ("a", 1, 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_middle(self):
        list1 = List.objects.filter(pk=1).first()
        item_1_1 = Item(name="new", list=list1, order=2)
        item_1_1.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("", 0, 1, 2, 7), ("a", 1, 1, 3, 3), ("a", 1, 1, 4, 4), ("a", 1, 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_seccond_last(self):
        list1 = List.objects.filter(pk=1).first()
        item_1_1 = Item(name="new", list=list1, order=4)
        item_1_1.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("", 0, 1, 2, 3), ("", 0, 1, 3, 4), ("", 0, 1, 4, 7), ("a", 1, 1, 5, 5)]
        self.assertEqual(result, expected_result)

    def test_insert_last(self):
        list1 = List.objects.filter(pk=1).first()
        item_1_1 = Item(name="new", list=list1, order=5)
        item_1_1.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("", 0, 1, 2, 3), ("", 0, 1, 3, 4), ("", 0, 1, 4, 5), ("", 0, 1, 5, 7)]
        self.assertEqual(result, expected_result)
