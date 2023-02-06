from django.urls import path
from .views import *

urlpatterns = [
    path('addproduct/',create_product.as_view()), 
    path('listproducts/',list_product.as_view()),
    path('productdetails/<int:id>',get_product_details.as_view()),
    path('editproduct/<int:id>',edit_product.as_view()),
]