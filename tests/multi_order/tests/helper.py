from tests.multi_order.models import List, Item


def set_up_helper():
    list = List(name="list one")
    list.save()
    item = Item(name="lol", list=list)
    item.save()
    item = Item(name="aaa", list=list)
    item.save()
    item = Item()
    item.name = "yey"
    item.list = list
    item.save()

    list = List(name="list two")
    list.save()
    item = Item(name="ugh", list=list)
    item.save()
