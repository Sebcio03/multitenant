from rest_framework.routers import DefaultRouter

from api.customers.views import CustomerViewSet

router = DefaultRouter()
router.register("", CustomerViewSet, basename="customers")

urlpatterns = router.urls
