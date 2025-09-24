from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        items = data.get("items", [])
        formatted_items = []
        for it in items:
            pid = it.get("product_id") or it.get("product")
            if not pid:
                return Response({"detail": "product_id missing in item"}, status=status.HTTP_400_BAD_REQUEST)
            product = get_object_or_404(Product, pk=pid)
            formatted_items.append({"product": product, "quantity": int(it.get("quantity", 1))})
        order_data = {
            "user": request.user.id if request.user and request.user.is_authenticated else None,
            "address": data.get("address", ""),
            "items": formatted_items,
        }
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
