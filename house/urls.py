from django.urls import path, include
from rest_framework import routers

from house.views import *

router = routers.DefaultRouter()
router.register(r'house', HouseViewSet, basename='house')
router.register(r'floor', FloorViewSet, basename='floor')
router.register(r'section', SectionViewSet, basename='section')
router.register(r'corps', CorpsViewSet, basename='corps')
router.register(r'document', DocumentViewSet, basename='document')
router.register(r'news', NewsViewSet, basename='news')


urlpatterns = [
    path('', include(router.urls))
]