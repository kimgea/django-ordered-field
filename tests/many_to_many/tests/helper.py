from tests.many_to_many.models import (Product, Category, ProductCategory)


def set_up_helper():
    clothes = Category.objects.create(name="Clothes")
    sporting_goods = Category.objects.create(name="Sporting Goods")

    bat = Product.objects.create(name="Bat")
    bat_in_sporting_goods = ProductCategory.objects.create(product=bat,
                                                                category=sporting_goods)

    cap = Product.objects.create(name="Cap")
    cap_in_sporting_goods = ProductCategory.objects.create(product=cap,
                                                                category=sporting_goods)
    cap_in_clothes = ProductCategory.objects.create(product=cap, category=clothes)

    glove = Product.objects.create(name="Glove")
    glove_in_sporting_goods = ProductCategory.objects.create(product=glove,
                                                                  category=sporting_goods)

    tshirt = Product.objects.create(name="T-shirt")
    tshirt_in_clothes = ProductCategory.objects.create(product=tshirt,
                                                            category=clothes)

    jeans = Product.objects.create(name="Jeans")
    jeans_in_clothes = ProductCategory.objects.create(product=jeans,
                                                           category=clothes)

    jersey = Product.objects.create(name="Jersey")
    jersey_in_sporting_goods = ProductCategory.objects.create(product=jersey,
                                                                   category=sporting_goods)
    jersey_in_clothes = ProductCategory.objects.create(product=jersey,
                                                            category=clothes)

    ball = Product.objects.create(name="Ball")
    ball_in_sporting_goods = ProductCategory.objects.create(product=ball,
                                                                 category=sporting_goods)
