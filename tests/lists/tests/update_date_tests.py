import time

from django.test import TestCase

from tests.lists.models import Item
from tests.lists.tests.helper import set_up_helper


class ListUpdateDateTest(TestCase):
    """
    NB: this is a slow test...
    Im cheating and commenting it out most of the tests to increase speed. Not good
    TODO: find a way to mock or manually set the timezone object time for faster testing

    TODO: check that date works for delete and inser also
    """
    def setUp(self):
        set_up_helper()
        self.pre_result = list(
            Item.objects.filter(list=1).order_by("order").
            values_list("id", "created", "updated", "order"))
        time.sleep(1)

    def _assert_helper(self, changed):
        post_result = list(
            Item.objects.order_by("list", "id").
            values_list("id", "created", "updated", "list", "order"))

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

    def test_created_is_the_same(self):
        item = Item(name="gg", list_id=1, order=0)
        item.save()

        post_result_created = list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "created", "order"))

        self.assertEqual(post_result_created,
                         [
                             (item.id, item.created, 0),
                             (1, self.pre_result[0][1], 1),
                             (2, self.pre_result[1][1], 2),
                             (3, self.pre_result[2][1], 3),
                             (4, self.pre_result[3][1], 4),
                             (5, self.pre_result[4][1], 5)
                         ])

    def test_change_order_first_to_second(self):
        item = Item.objects.filter(list=1, order=0).first()
        item.order = 1
        item.save()

        post_result= list(
            Item.objects.filter(list=1).order_by("order").
                values_list("id", "updated", "order"))

        # Changed
        self.assertNotEqual(post_result[0][1], self.pre_result[1][2])
        self.assertNotEqual(post_result[1][1], self.pre_result[0][2])
        # Not changed
        self.assertEqual(post_result[2][1], self.pre_result[2][2])
        self.assertEqual(post_result[3][1], self.pre_result[3][2])
        self.assertEqual(post_result[4][1], self.pre_result[4][2])


