from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Viewsets
from .views import ProductViewSet, OrderViewSet, RegisterView

# Simple JWT token views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Try to use a custom EmailTokenObtainPairSerializer (optional).
# If you've added EmailTokenObtainPairSerializer into store/serializers.py
# (see earlier suggestion), this will create a Token view that allows
# logging in with email or username. If not present, we fall back to the
# default TokenObtainPairView.
try:
    from .serializers import EmailTokenObtainPairSerializer
    from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView

    class EmailTokenObtainPairView(_TokenObtainPairView):
        serializer_class = EmailTokenObtainPairSerializer

    TokenView = EmailTokenObtainPairView
except Exception:
    # If the custom serializer/view isn't available, use the default token view
    TokenView = TokenObtainPairView


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    # Registration (creates a new user)
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    # Obtain tokens (access & refresh). If you implemented the optional
    # EmailTokenObtainPairSerializer, this route will accept email or username.
    path("auth/token/", TokenView.as_view(), name="token_obtain_pair"),
    # Refresh access token
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
