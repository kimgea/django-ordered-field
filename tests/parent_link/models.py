from django.db import models

from django_ordered_field import (OrderedCollectionField, OrderedField)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = OrderedCollectionField(collection='course', parent_link_name='unit_ptr')


class Video(Unit):
    description = models.CharField(max_length=100)


class Quiz(Unit):
    questions = models.CharField(max_length=100)


#########################

class UnitTwo(models.Model):
    name = models.CharField(max_length=100)
    position = OrderedField(parent_link_name='unittwo_ptr_id')


class VideoTwo(UnitTwo):
    description = models.CharField(max_length=100)


class QuizTwo(UnitTwo):
    questions = models.CharField(max_length=100)
