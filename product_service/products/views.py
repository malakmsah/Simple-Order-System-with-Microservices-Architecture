from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .services.product_service import ProductService

class ProductListCreateView(APIView):
    # GET: public, POST: admin only
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = ProductService.list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only allow admin users
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Admin credentials required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = ProductService.get_product(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
