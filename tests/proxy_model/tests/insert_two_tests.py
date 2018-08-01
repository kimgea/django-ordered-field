from django.test import TestCase

from tests.proxy_model.models import (PersonTwoProxy, PersonTwo)
from tests.proxy_model.tests.helper import set_up_helper_two


class InsertProxyTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_insert_main_lookup_proxy(self):
        video = PersonTwo(name="Person new", description="new", position=0)
        video.save()

        result = list(PersonTwoProxy.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person new", 0, 4),
                           ("Person 1", 1, 1),
                           ("Person 2", 2, 2),
                           ("Person 3", 3, 3)]
        self.assertEqual(result, expected_result)

    def test_insert_proxy_lookup_main(self):
        quiz = PersonTwoProxy(name="Person new", description="new", position=0)
        quiz.save()

        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person new", 0, 4),
                           ("Person 1", 1, 1),
                           ("Person 2", 2, 2),
                           ("Person 3", 3, 3)]
        self.assertEqual(result, expected_result)



