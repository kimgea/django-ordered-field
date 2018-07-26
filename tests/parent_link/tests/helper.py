from tests.parent_link.models import (Course, Video, Quiz)
from tests.parent_link.models import (VideoTwo, QuizTwo)


def set_up_helper():
    course = Course.objects.create(name="My Course")

    v1 = Video.objects.create(course=course, name="Video 1", description="Introduction")
    q1 = Quiz.objects.create(course=course, name="Quiz 1", questions="question 1")

    v2 = Video.objects.create(course=course, name="Video 2", description="mid")
    q2 = Quiz.objects.create(course=course, name="Quiz 2", questions="question 2")

    v3 = Video.objects.create(course=course, name="Video 3", description="end")
    q3 = Quiz.objects.create(course=course, name="Quiz 3", questions="question 3")


def set_up_helper_two():
    #vv = VideoTwo()
    #print(vv.__dict__)
    v1 = VideoTwo.objects.create(name="Video 1", description="Introduction")
    q1 = QuizTwo.objects.create(name="Quiz 1", questions="question 1")

    v2 = VideoTwo.objects.create(name="Video 2", description="mid")
    q2 = QuizTwo.objects.create(name="Quiz 2", questions="question 2")

    v3 = VideoTwo.objects.create(name="Video 3", description="end")
    q3 = QuizTwo.objects.create(name="Quiz 3", questions="question 3")
