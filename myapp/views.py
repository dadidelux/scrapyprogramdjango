from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.generics import ListCreateAPIView
from .serializers import ProductDataSerializer
from .models import ProductData
from rest_framework.pagination import PageNumberPagination

# Create your views here.
def productdata(request: HttpRequest):
    response = {
        "message": "Hello World"
    }
    return JsonResponse(data=response)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductDataListView(ListCreateAPIView):
    queryset = ProductData.objects.all()
    serializer_class = ProductDataSerializer
    pagination_class = CustomPageNumberPagination
