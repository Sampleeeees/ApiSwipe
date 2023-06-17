from django.db.models.expressions import NoneType
from django.utils.translation import gettext_lazy as _
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.exceptions import ObjectDoesNotExist
from message.models import Message
from gallery.models import Image
from house.models import *
from flat.models import *


class CustomIsAuthenticate(IsAuthenticated):
    message = _('У вас немає дозволу')

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

class IsAdminPermission(BasePermission):
    message = _('Ви не адміністратор та не маєте доступу до цього')

    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.role.is_admin
        except:
            return False

    def has_object_permission(self, request, view, obj):
        return True

class IsBuilderPermission(BasePermission):
    message = _('Ви не є забудовником і не маєте дозволу до цього')

    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.role.is_builder
        except:
            return False


    def has_object_permission(self, request, view, obj):
        return True

class IsManagerPermission(BasePermission):
    message = _('Ви не є менеджером і не маєте дозволу до цього')

    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.role.is_manager
        except:
            return False

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerPermission(BasePermission):
    message = _('Ви не є валсником')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (House, Section, Floor, Corps, News, Document)):
            return request.user == obj.builder
        elif isinstance(obj, Flat):
            return request.user == obj.user
#        elif isinstance(obj, (SavedFilters, Favorites)):
#            return request.user == obj.user
        else:
            return False

class IsSenderPermission(BasePermission):
    message = _('Ви не відправляли повідомлення')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return request.user == obj.user_sender
        return False
