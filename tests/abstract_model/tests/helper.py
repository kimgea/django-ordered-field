from tests.abstract_model.models import (Course, Person)
from tests.abstract_model.models import (PersonTwo)


def set_up_helper():
    course = Course.objects.create(name="My Course")

    Person.objects.create(course=course, name="Person 1", description="Introduction")
    Person.objects.create(course=course, name="Person 2", description="mid")
    Person.objects.create(course=course, name="Person 3", description="end")


def set_up_helper_two():
    PersonTwo.objects.create(name="Person 1", description="Introduction")
    PersonTwo.objects.create(name="Person 2", description="mid")
    PersonTwo.objects.create(name="Person 3", description="end")
