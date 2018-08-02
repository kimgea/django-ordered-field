from django.test import TestCase

from tests.abstract_model.models import (Person)
from tests.abstract_model.tests.helper import set_up_helper


class ChangeAbstractTests(TestCase):
    def setUp(self):
        set_up_helper()

    def test_person_update(self):
        item = Person.objects.filter(pk=1).first()
        item.position = -1
        item.save()
        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 2", 0, 2),
                           (1, "Person 3", 1, 3),
                           (1, "Person 1", 2, 1)]
        self.assertEqual(result, expected_result)
