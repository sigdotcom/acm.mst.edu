from ACM_General.accounts.models import User, Group, Permission
from ACM_General.accounts.serializers import UserSerializer, GroupSerializer, PermissionSerializer
from ACM_General.events.models import Event
from ACM_General.events.serializers import EventSerializer
from ACM_General.sigs.models import SIG
from ACM_General.sigs.serializers import SIGSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_api.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import filters


class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    List all Users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, updates, or delete a User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    List all Events or create a new event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = filters.EventFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    """
    Retrieve, updates, or delete a Event instance.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SIGList(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              generics.GenericAPIView):
    """
    List all SIGs or create a new sig.
    """
    queryset = SIG.objects.all()
    serializer_class = SIGSerializer
    filter_class = filters.SIGFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SIGDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    """
    Retrieve, updates, or delete a SIG instance.
    """
    queryset = SIG.objects.all()
    serializer_class = SIGSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
