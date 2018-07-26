from django.db import models

from django_ordered_field import OrderedCollectionField
from django_ordered_field import OrderedField

class List(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey('List', related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = OrderedCollectionField(collection=['list'],
                                   extra_field_updates={
                                       'order_changed_count': models.F("order_changed_count") + 1,
                                   }
                                   )
    order_changed_count = models.IntegerField(default=0)
    rank = OrderedField(extra_field_updates={
        'rank_changed_count': models.F("rank_changed_count") + 1
    })
    rank_changed_count = models.IntegerField(default=0)

    """__original_order = None

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.__original_order = self.order"""

    def __unicode__(self):
        return str(self.name) + " (List: " + self.list.name + ", position: " + str(self.order) + ")"

    """def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.order != self.__original_order:
            pass

        instance = super(Item, self).save(force_insert, force_update, using, update_fields)
        self.__original_order = self.order
        return instance"""
