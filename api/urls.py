from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageModelViewSet

router = DefaultRouter()
router.register('predict', ImageModelViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
