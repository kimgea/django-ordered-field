from django.db import models

from django_ordered_field import (OrderedCollectionField, OrderedField, add_signals)
from django.db.models.signals import (post_delete, post_save, pre_delete, pre_save)


class Course(models.Model):
    name = models.CharField(max_length=100)


class CommonInfo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = OrderedCollectionField(collection='course')

    class Meta:
        abstract = True


class Person(CommonInfo):
    description = models.CharField(max_length=100)


#add_signals(CommonInfo, Person, "position")



#########################

class CommonInfoTwo(models.Model):
    name = models.CharField(max_length=100)
    position = OrderedField()

    class Meta:
        abstract = True


class PersonTwo(CommonInfoTwo):
    description = models.CharField(max_length=100)







