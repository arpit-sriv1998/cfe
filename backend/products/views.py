from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF View
    """
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            print(instance)
            return Response(
                {
                    "stautus": "success",
                    "message": "Product created successfully",
                    "data": serializer.data,
                },
                status=201
            )
        return Response(
            {
                "stautus": "failure",
                "message": serializer.errors,
                "data": None,
            },
            status=400
        )
    except Exception as e:
        return Response(
            {
                "stautus": "failure",
                "message": str(e),
                "data": None,
            },
            status=500
        )
