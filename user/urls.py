from rest_framework import routers
from django.urls import path, include
from .views import SubscriptionViewSet, UserViewSet, NotaryViewSet


router = routers.DefaultRouter()
router.register(r'subscription', SubscriptionViewSet, basename='subscription')
router.register(r'user', UserViewSet, basename='user')
router.register(r'notary', NotaryViewSet, basename='notary')

urlpatterns = [
    path('', include(router.urls))
]