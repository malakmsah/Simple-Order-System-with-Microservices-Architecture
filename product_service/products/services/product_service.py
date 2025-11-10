from products.models import Product
from rest_framework.exceptions import NotFound, ValidationError

class ProductService:
    @staticmethod
    def list_products():
        return Product.objects.all()

    @staticmethod
    def get_product(product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

    @staticmethod
    def create_product(validated_data):
        price = validated_data.get("price")
        stock = validated_data.get("stock")

        if price <= 0 or stock < 0:
            raise ValidationError("Invalid product data")

        return Product.objects.create(**validated_data)
