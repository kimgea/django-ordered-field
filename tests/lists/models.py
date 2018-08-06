from django.db import models

from django_ordered_field import OrderedCollectionField



def get_loged_in_user():
    return "a"

class List(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey('List', related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    order = OrderedCollectionField(collection='list',
                                   extra_field_updates={
                                       'order_changed_count': models.F("order_changed_count") + 1,
                                       'updated_by': get_loged_in_user
                                   },
                                   self_updates_on_collection_change={
                                       'change_collection_count': models.F("change_collection_count") + 1
                                   })
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)
    order_changed_count = models.IntegerField(default=0)
    change_collection_count = models.IntegerField(default=0)

    """__original_order = None

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.__original_order = self.order"""

    def __unicode__(self):
        return str(self.name) + " (List: " + self.list.name + ", position: " + str(self.order) + ")"

    """def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.order != self.__original_order:
            self.order_changed_count += 1
            self.updated_by = get_loged_in_user()

        instance = super(Item, self).save(force_insert, force_update, using, update_fields)
        self.__original_order = self.order
        return instance"""


