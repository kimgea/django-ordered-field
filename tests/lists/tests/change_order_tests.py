from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper


class ListChangeOrderTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_change_order_first_to_second(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 1
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("a", 1, 1, 0, 2), ("a", 1, 1, 1, 1), ("", 0, 1, 2, 3), ("", 0, 1, 3, 4), ("", 0, 1, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_first_to_middle(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 2
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("a", 1, 1, 0, 2), ("a", 1, 1, 1, 3), ("a", 1, 1, 2, 1), ("", 0, 1, 3, 4), ("", 0, 1, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_first_to_last(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 4
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("a", 1, 1, 0, 2), ("a", 1, 1, 1, 3), ("a", 1, 1, 2, 4), ("a", 1, 1, 3, 5), ("a", 1, 1, 4, 1)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_one_up(self):
        item = Item.objects.filter(list=1, order=2).first()
        item.order = 1
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("a", 1, 1, 1, 3), ("a", 1, 1, 2, 2), ("", 0, 1, 3, 4), ("", 0, 1, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_one_down(self):
        item = Item.objects.filter(list=1, order=2).first()
        item.order = 3
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("a", 1, 1, 2, 4), ("a", 1, 1, 3, 3), ("", 0, 1, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_to_first(self):
        item = Item.objects.filter(list=1, order=2).first()
        item.order = 0
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("a", 1, 1, 0, 3), ("a", 1, 1, 1, 1), ("a", 1, 1, 2, 2), ("", 0, 1, 3, 4), ("", 0, 1, 4, 5)]
        self.assertEqual(result, expected_result)

    def test_change_order_middle_to_last(self):
        item = Item.objects.filter(list=1, order=2).first()
        item.order = 4
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("a", 1, 1, 2, 4), ("a", 1, 1, 3, 5), ("a", 1, 1, 4, 3)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_second_last(self):
        item = Item.objects.filter(list=1, order=4).first()
        item.order = 3
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("", 0, 1, 2, 3), ("a", 1, 1, 3, 5), ("a", 1, 1, 4, 4)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_middle(self):
        item = Item.objects.filter(list=1, order=4).first()
        item.order = 2
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("", 0, 1, 0, 1), ("", 0, 1, 1, 2), ("a", 1, 1, 2, 5), ("a", 1, 1, 3, 3), ("a", 1, 1, 4, 4)]
        self.assertEqual(result, expected_result)

    def test_change_order_last_to_first(self):
        item = Item.objects.filter(list=1, order=4).first()
        item.order = 0
        item.save()

        result = list(Item.objects.filter(list=1).order_by("list", "order").
                      values_list("updated_by", "order_changed_count", "list", "order", "id"))
        expected_result = [("a", 1, 1, 0, 5), ("a", 1, 1, 1, 1), ("a", 1, 1, 2, 2), ("a", 1, 1, 3, 3), ("a", 1, 1, 4, 4)]
        self.assertEqual(result, expected_result)
