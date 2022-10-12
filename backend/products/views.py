from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
# @api_view(['POST'])
# def api_home(request, *args, **kwargs):
#     """
#     DRF View
#     """
#     try:
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()
#             print(instance)
#             return Response(
#                 {
#                     "stautus": "success",
#                     "message": "Product created successfully",
#                     "data": serializer.data,
#                 },
#                 status=201
#             )
#         return Response(
#             {
#                 "stautus": "failure",
#                 "message": serializer.errors,
#                 "data": None,
#             },
#             status=400
#         )
#     except Exception as e:
#         return Response(
#             {
#                 "stautus": "failure",
#                 "message": str(e),
#                 "data": None,
#             },
#             status=500
#         )



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # print(serializer_class)
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None 
        # print(title, content)
        if content is None:
            content = title
        serializer.save(content=content)


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None 
        # print(title, content)
        if content is None:
            content = title
        serializer.save(content=content)


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




@api_view(['GET','POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 

    if method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            print(serializer.data)
            return Response(serializer.data)
        return Response({'invalid': 'not good data'}, status=400)





class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None 
            # print(title, content)
            if content is None:
                content = title
            serializer.save(content=content)







