from django.test import TestCase

from tests.multi_ordered.models import List, Item

class ChangeMultiCollectionTests(TestCase):
    def setUp(self):
        list_1 = List(name="list one")
        list_1.save()

        item_1_1 = Item(name="lol", list=list_1, sub_coll=1)
        item_1_1.save()

        item_1_2 = Item()
        item_1_2.name = "yey"
        item_1_2.list = list_1
        item_1_2.sub_coll = 2
        item_1_2.save()


        list_2 = List(name="list one")
        list_2.save()

        item_2_1 = Item(name="ugh", list=list_2, sub_coll=1)
        item_2_1.save()

    def test_one(self):
        list2 = List.objects.filter(pk=2).first()
        item = Item.objects.filter(list=1, order=0).first()
        item.list = list2
        item.order = -1
        item.save()

        result = list(Item.objects.order_by("list", "order").
                      values_list("list", "order", "id"))
        expected_result = [(1, 0, 2), (2, 0, 3), (2, 1, 1)]
        self.assertEqual(result, expected_result)
        #self.assertTrue(False)
