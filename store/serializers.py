from rest_framework import serializers
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "image_url", "external_image"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.external_image:
            return obj.external_image
        if obj.image and hasattr(obj.image, "url"):
            url = obj.image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total", "address", "items"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            product = item["product"]
            quantity = item["quantity"]
            price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total += price * quantity
        order.total = total
        order.save()
        return order

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"], email=validated_data.get("email"), password=validated_data["password"])
        return user

# append to backend/store/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Allow login by email or username.
    If 'username' field contains an email, substitute the matching username.
    """
    def validate(self, attrs):
        username = attrs.get("username")
        if username and "@" in username:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=username)
                # replace username with the user's username so parent serializer can authenticate
                attrs["username"] = user.username
            except User.DoesNotExist:
                # leave attrs as-is - parent will fail authentication and return 401
                pass
        return super().validate(attrs)
