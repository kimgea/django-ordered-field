from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper


class ListInitialOrderTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_init_order(self):
        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0)]
        self.assertEqual(result, expected_result)

    def test_init_order_list_one(self):
        result = list(Item.objects.filter(list_id=1).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
        self.assertEqual(result, expected_result)

    def test_init_order_list_two(self):
        result = list(Item.objects.filter(list_id=2).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(2, 0)]
        self.assertEqual(result, expected_result)
