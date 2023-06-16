from django.urls import path, include
from rest_framework import routers

from flat.views import FlatView

router = routers.DefaultRouter()
router.register(r'flat', FlatView, basename='flat')



urlpatterns = [
    path('', include(router.urls))
]