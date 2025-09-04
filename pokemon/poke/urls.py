from django.urls import path
from .views import (
    products, 
    product_details, 
    product_create, 
    product_update, 
    product_delete
)

urlpatterns = [
    path("", products, name="products"),
    path("detail/<int:product_id>/", product_details, name="pokemon_detail"),
    path("create/", product_create, name="pokemon_create"),
    path("update/<int:product_id>/", product_update, name="pokemon_update"),
    path("delete/<int:product_id>/", product_delete, name="pokemon_delete"),
]