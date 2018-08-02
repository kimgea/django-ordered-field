from django.test import TestCase

from tests.proxy_model.models import (PersonTwoProxy, PersonTwo)
from tests.proxy_model.tests.helper import set_up_helper_two

class DeleteProxyTwoTest(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_delete_main_lookup_proxy(self):
        item = PersonTwo.objects.filter(pk=1).first()
        item.delete()

        result = list(PersonTwoProxy.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3)]
        self.assertEqual(result, expected_result)

    def test_delete_proxy_lookup_main(self):
        item = PersonTwoProxy.objects.filter(pk=1).first()
        item.delete()

        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3)]
        self.assertEqual(result, expected_result)



