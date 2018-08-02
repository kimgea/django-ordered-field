from django.test import TestCase

from tests.many_to_many.models import (Product, Category, ProductCategory)
from tests.many_to_many.tests.helper import set_up_helper


class ChangeManyToManyTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_update_m2m(self):
        m2m = ProductCategory.objects.filter(position=0, category_id=1).first()
        m2m.position = -1
        m2m.save()

        actual_order = list(ProductCategory.objects.filter(category_id=1).
                            values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'T-shirt', 0), (u'Jeans', 1), (u'Jersey', 2), (u'Cap', 3)]
        self.assertEqual(actual_order, expected_order)

    def test_update_m2m_not_affect_other_category(self):
        m2m = ProductCategory.objects.filter(position=0, category_id=1).first()
        m2m.position = -1
        m2m.save()

        actual_order = list(ProductCategory.objects.filter(category_id=2).
                            values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Cap', 1), (u'Glove', 2), (u'Jersey', 3), (u'Ball', 4)]
        self.assertEqual(actual_order, expected_order)

