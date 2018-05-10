from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper


class ListDeleteTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_first(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.delete()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 2), (1, 1, 3), (1, 2, 4), (1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_second(self):
        item = Item.objects.filter(list=1, order=1).first()
        item.delete()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 1), (1, 1, 3), (1, 2, 4), (1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_middle(self):
        item = Item.objects.filter(list=1, order=2).first()
        item.delete()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 1), (1, 1, 2), (1, 2, 4), (1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_second_last(self):
        item = Item.objects.filter(list=1, order=3).first()
        item.delete()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 1), (1, 1, 2), (1, 2, 3), (1, 3, 5)]
        self.assertEqual(result, expected_result)

    def test_delete_last(self):
        item = Item.objects.filter(list=1, order=4).first()
        item.delete()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 1), (1, 1, 2), (1, 2, 3), (1, 3, 4)]
        self.assertEqual(result, expected_result)
