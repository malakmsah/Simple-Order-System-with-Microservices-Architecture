from payments.models import Payment
from rest_framework.exceptions import ValidationError, NotFound

class PaymentService:
    @staticmethod
    def create_payment(order_id, amount):
        if amount <= 0:
            status = 'FAILED'
        else:
            status = 'COMPLETED'

        payment, created = Payment.objects.update_or_create(
            order_id=order_id,
            defaults={'amount': amount, 'status': status}
        )
        return payment

    @staticmethod
    def get_payment_by_order(order_id):
        try:
            return Payment.objects.get(order_id=order_id)
        except Payment.DoesNotExist:
            raise NotFound("Payment not found")
