from tests.proxy_model.models import (Course, Person)
from tests.proxy_model.models import PersonTwo


def set_up_helper():
    course = Course.objects.create(name="My Course")

    v1 = Person.objects.create(course=course, name="Person 1", description="Introduction")
    v2 = Person.objects.create(course=course, name="Person 2", description="mid")
    v3 = Person.objects.create(course=course, name="Person 3", description="end")


def set_up_helper_two():
    v1 = PersonTwo.objects.create(name="Person 1", description="Introduction")
    v2 = PersonTwo.objects.create(name="Person 2", description="mid")
    v3 = PersonTwo.objects.create(name="Person 3", description="end")
