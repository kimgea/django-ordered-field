from django.db import models

from django_ordered_field import OrderedField

def get_loged_in_user():
    return "a"

class HearthstoneRanking(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rank = OrderedField(extra_field_updates={
                                       'order_changed_count': models.F("order_changed_count") + 1,
                                       'updated_by': get_loged_in_user
                                   })
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)
    order_changed_count = models.IntegerField(default=0)

    """__original_rank = None

    def __init__(self, *args, **kwargs):
        super(HearthstoneRanking, self).__init__(*args, **kwargs)
        self.__original_rank = self.rank"""


    """def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.rank != self.__original_rank:
            self.updated_by = get_loged_in_user()

        instance = super(HearthstoneRanking, self).save(force_insert, force_update, using, update_fields)
        self.__original_rank = self.rank
        return instance"""
