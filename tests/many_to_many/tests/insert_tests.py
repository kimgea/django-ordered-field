from django.test import TestCase

from tests.many_to_many.models import (Product, Category, ProductCategory)
from tests.many_to_many.tests.helper import set_up_helper


class InsertManyToManyTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_init_category_clothes(self):
        actual_order = list(ProductCategory.objects.filter(category_id=1).
            values_list('product__name','position').order_by('position'))
        expected_order = [(u'Cap', 0), (u'T-shirt', 1), (u'Jeans', 2), (u'Jersey', 3)]
        self.assertEqual(actual_order, expected_order)

    def test_init_category_sporting_goods(self):
        actual_order = list(ProductCategory.objects.filter(category_id=2).
            values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Cap', 1), (u'Glove', 2), (u'Jersey', 3), (u'Ball', 4)]
        self.assertEqual(actual_order, expected_order)

    def test_insert_front(self):
        item = Product.objects.create(name="New")
        m2m = ProductCategory(product=item, category_id=1, position=0)
        m2m.save()

        actual_order = list(ProductCategory.objects.filter(category_id=1).
                            values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'New', 0), (u'Cap', 1), (u'T-shirt', 2), (u'Jeans', 3), (u'Jersey', 4)]
        self.assertEqual(actual_order, expected_order)

    def test_insert_front_not_affect_other_category(self):
        item = Product.objects.create(name="New")
        ProductCategory.objects.create(product=item, category_id=1, position=0)

        actual_order = list(ProductCategory.objects.filter(category_id=2).
                            values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Cap', 1), (u'Glove', 2), (u'Jersey', 3), (u'Ball', 4)]
        self.assertEqual(actual_order, expected_order)



