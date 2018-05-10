from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper


class ListInitialQueryTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_init_query_order_multiple(self):
        result = list(Item.objects.filter(order=0).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 0), (2, 0)]
        self.assertEqual(result, expected_result)

    def test_init_query_order_single(self):
        result = list(Item.objects.filter(order=1).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 1)]
        self.assertEqual(result, expected_result)

    def test_init_query_order_on_list_before_first(self):
        result = list(Item.objects.filter(list=1, order=-1).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_init_query_order_on_list_first(self):
        result = list(Item.objects.filter(list=1, order=0).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 0)]
        self.assertEqual(result, expected_result)

    def test_init_query_order_on_list_middle(self):
        result = list(Item.objects.filter(list=1, order=2).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 2)]
        self.assertEqual(result, expected_result)

    def test_init_query_order_on_list_last(self):
        result = list(Item.objects.filter(list=1, order=4).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = [(1, 4)]
        self.assertEqual(result, expected_result)

    def test_init_query_order_on_list_after_last(self):
        result = list(Item.objects.filter(list=1, order=-5).order_by("list", "order").
                      values_list("list", "order"))
        expected_result = []
        self.assertEqual(result, expected_result)
