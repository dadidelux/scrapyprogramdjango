from . import views
from django.urls import path
from .views import ProductDataListView

urlpatterns = [
    path("productdata/", views.productdata, name="productdata"),
    path('products/', ProductDataListView.as_view(), name='product-list'),
]

