from rest_framework import routers
from main import views as order_views

router = routers.DefaultRouter()
router.register(r'order' , order_views.OrderViewSet)