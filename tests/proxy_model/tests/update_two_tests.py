from django.test import TestCase

from tests.proxy_model.models import (PersonTwoProxy, PersonTwo)
from tests.proxy_model.tests.helper import set_up_helper_two


class ChangeProxyTwoTests(TestCase):
    def setUp(self):
        set_up_helper_two()

    def test_video_update(self):
        video = PersonTwo.objects.filter(pk=1).first()
        video.position = -1
        video.save()
        result = list(PersonTwoProxy.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3),
                           ("Person 1", 2, 1)]
        self.assertEqual(result, expected_result)

    def test_quiz_update(self):
        quiz = PersonTwoProxy.objects.filter(pk=1).first()
        quiz.position = -1
        quiz.save()
        result = list(PersonTwo.objects.all().order_by("position").
                      values_list("name", "position", "id"))
        expected_result = [("Person 2", 0, 2),
                           ("Person 3", 1, 3),
                           ("Person 1", 2, 1)]
        self.assertEqual(result, expected_result)

