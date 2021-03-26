from django.urls import path
from store.views import (
        home, 
        category,
        sub_category,
        product_detail, 
        add_to_basket, 
        my_basket,
        add_item,
        delete_item,
        shipping_address,
        shop_by_brand,
        brand_name,
        payment
    )

app_name = "store"


urlpatterns = [
    path("", home, name="home"),
    path("product/<int:pk>/category/", category, name="category"),
    path("product/<int:pk>/sub_category/", sub_category, name="sub_category"),
    path("shop_by_brand/", shop_by_brand, name="shop_by_brand"),
    path("brand_name/<int:pk>/", brand_name, name="brand_name"),
    path("product/<int:pk>/detail/", product_detail, name="product_detail"),
    path("product/<int:pk>/add_to_basket/", add_to_basket, name="add_to_basket"),
    path("user/<int:pk>/basket/", my_basket, name="my_basket"),
    path("add/item/<int:pk>/", add_item, name="add_item"),
    path("delete/item/<int:pk>/", delete_item, name="delete_item"),
    path("shipping_address/",shipping_address, name="shipping_address"),
    path("payment/", payment, name="payment"),
]
