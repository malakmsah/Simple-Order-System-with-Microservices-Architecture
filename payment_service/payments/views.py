from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from .services.payment_service import PaymentService

class PaymentCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        if not order_id or amount is None:
            return Response({"error": "order_id and amount required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = PaymentService.create_payment(order_id, float(amount))
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, order_id):
        try:
            payment = PaymentService.get_payment_by_order(order_id)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
