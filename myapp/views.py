from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
##
from rest_framework.generics import ListAPIView
from .models import ProductData
from .serializers import ProductDataSerializer

# Create your views here.
def productdata(request:HttpRequest):
    response={
        "message":"Hello World"
    }
    return JsonResponse(data=response)


class ProductDataListAPIView(ListAPIView):
    queryset = ProductData.objects.all()
    serializer_class = ProductDataSerializer