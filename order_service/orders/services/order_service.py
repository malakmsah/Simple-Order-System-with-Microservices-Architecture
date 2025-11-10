import requests
import logging
from decimal import Decimal
from orders.models import Order
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

PRODUCT_SERVICE_URL = 'http://localhost:8001/api/products/'
PAYMENT_SERVICE_URL = 'http://localhost:8002/api/payments/'

class OrderService:

    @staticmethod
    def fetch_product(product_id):
        try:
            resp = requests.get(f"{PRODUCT_SERVICE_URL}{product_id}/", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching product {product_id}: {e}")
            return None

    @staticmethod
    def reserve_stock(products):
        # Reduce stock immediately, simulate via POST to Product Service if needed
        # Here, we assume stock is reduced in memory for simplicity
        for p in products:
            if p['stock'] <= 0:
                raise ValidationError(f"Product {p['name']} is out of stock.")

    @staticmethod
    def create_payment(order_id, total_amount):
        retries = 2
        for attempt in range(retries + 1):
            try:
                resp = requests.post(PAYMENT_SERVICE_URL, json={
                    'order_id': str(order_id),
                    'amount': float(total_amount)
                }, timeout=5)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Payment attempt {attempt+1} failed: {e}")
                if attempt == retries:
                    return None

    @staticmethod
    def create_order(customer_name, product_ids):
        order = Order(customer_name=customer_name)
        products = []

        # Fetch and validate products
        for pid in product_ids:
            p = OrderService.fetch_product(pid)
            if not p:
                order.status = 'CANCELLED'
                order.cancellation_reason = f"Product {pid} not found"
                order.save()
                return order
            products.append(p)

        # Reserve stock
        try:
            OrderService.reserve_stock(products)
        except ValidationError as ve:
            order.status = 'CANCELLED'
            order.cancellation_reason = str(ve)
            order.save()
            return order

        # Calculate total
        total_amount = sum(Decimal(p['price']) for p in products)
        order.total_amount = total_amount
        order.save()

        # Create payment
        payment_response = OrderService.create_payment(order.id, total_amount)
        if not payment_response or payment_response.get('status') != 'COMPLETED':
            order.status = 'CANCELLED'
            order.cancellation_reason = 'Payment failed'
            order.save()
            return order

        order.status = 'PAID'
        order.save()
        return order

    @staticmethod
    def get_order_details(order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

        # Fetch payment status
        try:
            resp = requests.get(f"{PAYMENT_SERVICE_URL}{order_id}/", timeout=5)
            payment_status = resp.json().get('status') if resp.status_code == 200 else None
        except requests.exceptions.RequestException:
            payment_status = None

        return {
            'order': order,
            'payment_status': payment_status
        }
