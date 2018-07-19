from tests.ordered_table.models import HearthstoneRanking


def set_up_helper():
    item_1_1 = HearthstoneRanking()
    item_1_1.name = "kim85"
    item_1_1.description = "Worlds greatest hearthstone player. Even if he never have reached legendary."
    item_1_1.save()

    item_1_2 = HearthstoneRanking()
    item_1_2.name = "StanCifka"
    item_1_2.description = "Not as good as number one :p"
    item_1_2.save()

    item_1_3 = HearthstoneRanking(name="Pavel")
    item_1_3.save()
    item_1_4 = HearthstoneRanking(name="Muzzy")
    item_1_4.save()
    item_1_5 = HearthstoneRanking(name="Xixo")
    item_1_5.save()

    """result = list(HearthstoneRanking.objects.all().order_by("rank").
                  values_list("rank", "id"))

    print(result)"""

