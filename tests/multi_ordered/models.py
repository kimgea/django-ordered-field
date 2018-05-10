from django.db import models

from django_ordered_field import OrderedCollectionField


class List(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey('List', related_name='items', on_delete=models.CASCADE)
    sub_coll = models.IntegerField()
    name = models.CharField(max_length=100)
    order = OrderedCollectionField(collection='list')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name) + " (List: " + self.list.name + ", position: " + str(self.order) + ")"
