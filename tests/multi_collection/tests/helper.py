from tests.multi_collection.models import List, Item


def set_up_helper():
    list = List(name="list one")
    list.save()

    item = Item(name="lol", list=list, sub_coll=1)
    item.save()
    item = Item(name="aaa", list=list, sub_coll=1)
    item.save()

    item = Item()
    item.name = "yey"
    item.list = list
    item.sub_coll = 2
    item.save()

    list = List(name="list two")
    list.save()

    item = Item(name="ugh", list=list, sub_coll=1)
    item.save()
