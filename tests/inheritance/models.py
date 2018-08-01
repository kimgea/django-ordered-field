from django.db import models

from django_ordered_field import (OrderedCollectionField, OrderedField, add_signals)
from django.db.models.signals import (post_delete, post_save, pre_delete, pre_save)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = OrderedCollectionField(collection='course')


class Video(Unit):
    description = models.CharField(max_length=100)


add_signals(Unit, Video, "position")


class Quiz(Unit):
    questions = models.CharField(max_length=100)


add_signals(Unit, Quiz, "position")


#########################

class UnitTwo(models.Model):
    name = models.CharField(max_length=100)
    position = OrderedField()


class VideoTwo(UnitTwo):
    description = models.CharField(max_length=100)


add_signals(UnitTwo, VideoTwo, "position")


class QuizTwo(UnitTwo):
    questions = models.CharField(max_length=100)


add_signals(UnitTwo, QuizTwo, "position")
