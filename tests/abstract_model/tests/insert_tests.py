from django.test import TestCase

from tests.abstract_model.models import (Person)
from tests.abstract_model.tests.helper import set_up_helper


class InsertAbstractTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_person_init(self):
        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 1", 0, 1),
                           (1, "Person 2", 1, 2),
                           (1, "Person 3", 2, 3)]
        self.assertEqual(result, expected_result)

    def test_person_insert_front(self):
        video = Person(course_id=1, name="Person new", description="new", position=0)
        video.save()

        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person new", 0, 4),
                           (1, "Person 1", 1, 1),
                           (1, "Person 2", 2, 2),
                           (1, "Person 3", 3, 3)]
        self.assertEqual(result, expected_result)




