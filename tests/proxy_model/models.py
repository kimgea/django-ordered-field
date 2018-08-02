from django.db import models

from django_ordered_field import (OrderedCollectionField, OrderedField, add_signals_for_proxy)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Person(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    position = OrderedCollectionField(collection='course')


class PersonProxy(Person):

    class Meta:
        proxy = True

    def do_something(self):
        return True


add_signals_for_proxy(Person, PersonProxy, "position")    # argh.. special for proxy too. Delete is included on inheritance but not on proxy



#########################

class PersonTwo(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    position = OrderedField()


class PersonTwoProxy(PersonTwo):

    class Meta:
        proxy = True

    def do_something(self):
        return True

add_signals_for_proxy(PersonTwo, PersonTwoProxy, "position")







