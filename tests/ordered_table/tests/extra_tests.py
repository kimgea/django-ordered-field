from types import MethodType

from django.test import TestCase
from django.db import models

from django_ordered_field import OrderedField
#from django_ordered_field.ordered_field import set_next_sibling

from tests.ordered_table.models import HearthstoneRanking
from tests.ordered_table.tests.helper import set_up_helper


def get_unique_together_class():
    class TestExceptionClass(models.Model):
        rank = OrderedField()
        group = models.IntegerField()

        class Meta:
            unique_together = ("rank", "group")
    return TestExceptionClass


class ListExtraTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_get_method(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        self.assertEqual(item.rank, 0)

    def test_get_method_getattr(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        self.assertEqual(getattr(item, "rank"), 0)

    def test_set_method_value_null(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        item.rank = None
        self.assertEqual(item.rank, -1)

    def test_set_method_setattr_value_null(self):
        item = HearthstoneRanking.objects.filter(rank=0).first()
        setattr(item, "rank", None)
        self.assertEqual(item.rank, -1)

    def test_order_field_cant_be_unique(self):
        asserted = False  # Ubgly, is there a asseetException???
        try:
            field = OrderedField(unique=True)
        except  TypeError:
            asserted = True
        self.assertTrue(asserted)

    def test_order_field_cant_be_in_unique_together(self):
        asserted = False  # Ubgly, is there a asseetException???
        try:
            m = get_unique_together_class()
        except  TypeError:
            asserted = True
        self.assertTrue(asserted)

    """def test_delete_when_next_sibling_has_been_deleted_by_other_process(self):
        def prepare_delete_new(sender, instance, **kwargs):
            self.assertEqual(item.rank, -1)

        item = HearthstoneRanking.objects.filter(rank=0).first()
        next_sibling = item._meta.get_field("rank").get_next_sibling(item)
        set_next_sibling(item, next_sibling, item._meta.get_field("rank").name)
        next_sibling.delete()
        OrderedField.prepare_delete = prepare_delete_new
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("rank", "id"))
        expected_result = [(0, 3), (1, 4), (2, 5)]
        self.assertEqual(result, expected_result)"""

    """def test_delete_when_next_siblings_has_been_deleted_by_other_process(self):
        def prepare_delete_new(sender, instance, **kwargs):
            self.assertEqual(item.rank, -1)

        item = HearthstoneRanking.objects.filter(rank=0).first()

        next_sibling = item._meta.get_field("rank").get_next_sibling(item)
        set_next_sibling(item, next_sibling, item._meta.get_field("rank").name)
        next_sibling.delete()
        next_sibling = item._meta.get_field("rank").get_next_sibling(item)
        set_next_sibling(item, next_sibling, item._meta.get_field("rank").name)
        next_sibling.delete()

        OrderedField.prepare_delete = prepare_delete_new
        item.delete()

        result = list(HearthstoneRanking.objects.order_by("rank").
                      values_list("rank", "id"))
        expected_result = [(0, 4), (1, 5)]
        self.assertEqual(result, expected_result)"""




