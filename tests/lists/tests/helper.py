from tests.lists.models import List, Item


def set_up_helper():
    list_1 = List(name="list one")
    list_1.save()

    item_1_1 = Item(name="lol", list=list_1)
    item_1_1.save()

    item_1_2 = Item()
    item_1_2.name = "yey"
    item_1_2.list = list_1
    item_1_2.save()

    item_1_3 = Item(name="lol 2", list=list_1)
    item_1_3.save()
    item_1_4 = Item(name="lol 3", list=list_1)
    item_1_4.save()
    item_1_5 = Item(name="lol 4", list=list_1)
    item_1_5.save()

    list_2 = List(name="list one")
    list_2.save()
    item_2_1 = Item(name="ugh", list=list_2)
    item_2_1.save()
