from django.test import TestCase

from tests.abstract_model.models import (PersonTwo)
from tests.abstract_model.tests.helper import set_up_helper_two


class InsertAbstractTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_person_init(self):
        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 1", 0, 1),
                           ("Person 2", 1, 2),
                           ("Person 3", 2, 3)]
        self.assertEqual(result, expected_result)

    def test_person_insert_front(self):
        video = PersonTwo(name="Person new", description="new", position=0)
        video.save()

        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person new", 0, 4),
                           ("Person 1", 1, 1),
                           ("Person 2", 2, 2),
                           ("Person 3", 3, 3)]
        self.assertEqual(result, expected_result)



