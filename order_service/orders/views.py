from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .services.order_service import OrderService

class OrderCreateView(APIView):

    def post(self, request):
        customer_name = request.data.get('customer_name')
        product_ids = request.data.get('product_ids', [])

        if not customer_name or not product_ids:
            return Response({'error': 'customer_name and product_ids required'}, status=status.HTTP_400_BAD_REQUEST)

        order = OrderService.create_order(customer_name, product_ids)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED if order.status != 'CANCELLED' else status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):

    def get(self, request, order_id):
        data = OrderService.get_order_details(order_id)
        if not data:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(data['order'])
        response = serializer.data
        response['payment_status'] = data['payment_status']
        return Response(response)
