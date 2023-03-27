from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("product", views.ProductViewSet)

urlpatterns = router.urls
