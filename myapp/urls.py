from . import views
from django.urls import path
from .views import ProductDataListAPIView

urlpatterns = [
    path("productdata/", views.productdata, name="productdata"),
    path('products/', ProductDataListAPIView.as_view(), name='product-list'),
]

