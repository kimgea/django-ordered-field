from django.test import TestCase

from tests.proxy_model.models import (PersonProxy, Person)
from tests.proxy_model.tests.helper import set_up_helper

class DeleteProxyTest(TestCase):
    def setUp(self):
        set_up_helper()

    def test_delete_main_lookup_proxy(self):
        item = Person.objects.filter(pk=1).first()
        item.delete()

        result = list(PersonProxy.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 2", 0, 2),
                           (1, "Person 3", 1, 3)]
        self.assertEqual(result, expected_result)

    def test_delete_proxy_lookup_main(self):
        item = PersonProxy.objects.filter(pk=1).first()
        item.delete()

        result = list(Person.objects.all().order_by("position").
                      values_list("course", "name", "position", "id"))
        expected_result = [(1, "Person 2", 0, 2),
                           (1, "Person 3", 1, 3)]
        self.assertEqual(result, expected_result)



