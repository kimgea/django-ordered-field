from django.test import TestCase
from django.db import models

from django_ordered_field import OrderedCollectionField

from tests.lists.models import List, Item
from tests.lists.tests.helper import set_up_helper


def get_no_collection_class():
    class TestExceptionClass(models.Model):
        rank = OrderedCollectionField(collection=None)
        group = models.IntegerField()
    return TestExceptionClass

class ListExtraTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_get_method(self):
        item = Item.objects.filter(list=1, order=4).first()
        id = item.id
        item.list = None
        item.save()

        item = Item.objects.filter(pk=id).first()

        self.assertEqual(item.list, None)
        self.assertEqual(item.order, 0)

        item2 = Item.objects.filter(list=1, order=0).first()
        id2 = item2.id
        item2.list = None
        item2.save()

        item2 = Item.objects.filter(pk=id2).first()
        item = Item.objects.filter(pk=id).first()

        self.assertEqual(item2.list, None)
        self.assertEqual(item2.order, 0)
        self.assertEqual(item.list, None)
        self.assertEqual(item.order, 1)


    def test_get_method2(self):
        item = Item.objects.filter(list=1, order=0).first()
        id = item.id
        item.list_id = 2
        item.save()

        item = Item.objects.filter(pk=id).first()

        self.assertEqual(item.list_id, 2)
        self.assertEqual(item.order, 0)

    def test_order_field_cant_be_in_unique_together(self):
        asserted = False  # Ubgly, is there a asseetException???
        try:
            m = get_no_collection_class()
        except  TypeError:
            asserted = True
        self.assertTrue(asserted)



