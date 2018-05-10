from django.test import TestCase

from tests.lists.models import List, Item
from tests.lists.tests.helper import set_up_helper


class ChangeCollectionTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_change_collection_to_back(self):
        list2 = List.objects.filter(pk=2).first()
        # for i in Item.objects.all():
        #    print(i.__dict__)
        item = Item.objects.filter(list=1, order=0).first()
        item.list = list2
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 2), (1, 1, 3), (1, 2, 4), (1, 3, 5), (2, 0, 6), (2, 1, 1)]
        self.assertEqual(result, expected_result)

    def test_change_collection_to_front(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item.objects.filter(list=1, order=0).first()
        item.list = list2
        item.order = 0
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 2), (1, 1, 3), (1, 2, 4), (1, 3, 5), (2, 0, 1), (2, 1, 6)]
        self.assertEqual(result, expected_result)
