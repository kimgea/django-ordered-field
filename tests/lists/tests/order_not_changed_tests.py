import time

from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper

class OrderNotChangedTest(TestCase):
    def setUp(self):
        set_up_helper()
        self.pre_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))
        #time.sleep(0.1)


    def test_change_order_not_changed(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.name = "KGA"
        item.save()

        post_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))


        self.assertEqual(post_result, self.pre_result)
