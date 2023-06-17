from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'filter', FilterViewSet, basename='filter')

urlpatterns = [
    path('', include(router.urls))
]