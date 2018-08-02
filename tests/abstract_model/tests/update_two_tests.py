from django.test import TestCase

from tests.abstract_model.models import (PersonTwo)
from tests.abstract_model.tests.helper import set_up_helper_two


class ChangeAbstractTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_person_update(self):
        item = PersonTwo.objects.filter(pk=1).first()
        item.position = -1
        item.save()
        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3),
                           ("Person 1", 2, 1)]
        self.assertEqual(result, expected_result)
