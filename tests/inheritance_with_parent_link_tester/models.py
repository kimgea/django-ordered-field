from django.db import models

from django_ordered_field import (OrderedCollectionField, OrderedField, add_signals_for_inheritance)
from django.db.models.signals import (post_delete, post_save, pre_delete, pre_save)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = OrderedCollectionField(collection='course', parent_link_name='unit_ptr')


class Video(Unit):
    description = models.CharField(max_length=100)


add_signals_for_inheritance(Unit, Video, "position")


class Quiz(Unit):
    questions = models.CharField(max_length=100)


add_signals_for_inheritance(Unit, Quiz, "position")


#########################

class UnitTwo(models.Model):
    name = models.CharField(max_length=100)
    position = OrderedField(parent_link_name='unittwo_ptr')


class VideoTwo(UnitTwo):
    description = models.CharField(max_length=100)


add_signals_for_inheritance(UnitTwo, VideoTwo, "position")


class QuizTwo(UnitTwo):
    questions = models.CharField(max_length=100)


add_signals_for_inheritance(UnitTwo, QuizTwo, "position")

