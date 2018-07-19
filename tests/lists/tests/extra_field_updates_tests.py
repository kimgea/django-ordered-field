import time

from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper
from django.utils.timezone import now

class ListExtraFieldUpdateTest(TestCase):
    def setUp(self):
        set_up_helper()
        self.pre_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))
        #time.sleep(0.1)

    def _assert_helper(self, changed):
        post_result = list(
            Item.objects.order_by("list", "id").
            values_list("id", "updated_by", "order_changed_count", "list", "order"))

        # created should stay the same
        self.assertEqual([(r[0], r[1]) for r in self.pre_result],
                         [(r[0], r[1]) for r in post_result])

        # Updated should change, but only on those that are changed
        for i in range(len(post_result)):  # Feels bad to check in loop
            if (post_result[i][3], post_result[i][4]) in changed:
                self.assertNotEqual(
                    (self.pre_result[i][0], self.pre_result[i][2]),
                    (post_result[i][0], post_result[i][2]))
            else:
                self.assertEqual(
                    (self.pre_result[i][0], self.pre_result[i][2]),
                    (post_result[i][0], post_result[i][2]))

    def test_change_order_first_to_second(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.printit = True
        item.order = 1
        item.save()

        post_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))

        #print("test_change_order_first_to_second")
        #print(post_result)

        self.assertEqual(post_result,
                         [(2, 'a', 1, 0),
                          (1, 'a', 1, 1),
                          (3, '', 0, 2),
                          (4, '', 0, 3),
                          (5, '', 0, 4)
                          ])

    def test_change_order_multiple_changes(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 1
        item.save()

        item = Item.objects.filter(list=1, order=1).first()
        item.order = 2
        item.save()

        item = Item.objects.filter(list=1, order=2).first()
        item.order = 3
        item.save()

        post_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))

        #print("test_change_order_multiple_changes")
        #print(post_result)
        self.assertEqual(post_result,
                         [(2, 'a', 1, 0),
                          (3, 'a', 1, 1),
                          (4, 'a', 1, 2),
                          (1, 'a', 3, 3),
                          (5, '', 0, 4)
                          ])


    """def test_change_order_multiple_changes(self):
        # FAILS... sould I fix it... might work if self extra updates are moved to pre_save... look into that first
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 1
        item.save()

        item.order = 2
        item.save()

        item.order = 3
        item.save()

        post_result = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated_by", "order_changed_count", "order"))

        self.assertEqual(post_result,
                         [(2, 'Kim-Georg Aase', 1, 0),
                          (3, 'Kim-Georg Aase', 1, 1),
                          (4, 'Kim-Georg Aase', 1, 2),
                          (1, 'Kim-Georg Aase', 3, 3),
                          (5, '', 0, 4)
                          ])"""
