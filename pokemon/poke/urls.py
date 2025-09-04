from django.urls import path
from .views import products, product_details

urlpatterns = [
   path("", products, name="products"),
   path("detail/<int:product_id>/", product_details, name="pokemon_detail"),
]