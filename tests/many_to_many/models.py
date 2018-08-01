from django.db import models

from django_ordered_field import (OrderedCollectionField)

# Tests are mostly stolen from https://github.com/jpwatts/django-positions/blob/master/examples/store


class Product(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='ProductCategory', related_name='categories')

    def __unicode__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = OrderedCollectionField(collection='category')

    class Meta(object):
        unique_together = ('product', 'category')

    def __unicode__(self):
        return u"%s in %s" % (self.product, self.category)

