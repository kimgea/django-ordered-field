from django.test import TestCase

from tests.abstract_model.models import (PersonTwo)
from tests.abstract_model.tests.helper import set_up_helper_two


class DeleteAbstractTwoTest(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_delete_person(self):
        item = PersonTwo.objects.filter(pk=1).first()
        item.delete()

        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3)]
        self.assertEqual(result, expected_result)


