from django.test import TestCase

from tests.proxy_model.models import (PersonProxy, Person)
from tests.proxy_model.tests.helper import set_up_helper


class InsertProxyTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_insert_main_lookup_proxy(self):
        video = Person(course_id=1, name="Person new", description="new", position=0)
        video.save()

        result = list(PersonProxy.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person new", 0, 4),
                           (1, "Person 1", 1, 1),
                           (1, "Person 2", 2, 2),
                           (1, "Person 3", 3, 3)]
        self.assertEqual(result, expected_result)

    def test_insert_proxy_lookup_main(self):
        quiz = PersonProxy(course_id=1, name="Person new", description="new", position=0)
        quiz.save()

        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person new", 0, 4),
                           (1, "Person 1", 1, 1),
                           (1, "Person 2", 2, 2),
                           (1, "Person 3", 3, 3)]
        self.assertEqual(result, expected_result)



