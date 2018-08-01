from django.test import TestCase

from tests.proxy_model.models import (PersonProxy, Person)
from tests.proxy_model.tests.helper import set_up_helper


class ChangeProxyTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_update_main_lookup_proxy(self):
        video = Person.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(PersonProxy.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 2", 0, 2),
                           (1, "Person 3", 1, 3),
                           (1, "Person 1", 2, 1)]
        self.assertEqual(result, expected_result)

    def test_update_proxy_lookup_main(self):
        quiz = PersonProxy.objects.filter(pk=1).first()
        quiz.position = -1
        quiz.save()
        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 2", 0, 2),
                           (1, "Person 3", 1, 3),
                           (1, "Person 1", 2, 1)]
        self.assertEqual(result, expected_result)

