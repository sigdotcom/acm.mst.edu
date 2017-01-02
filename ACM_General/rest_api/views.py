from accounts.models import User 
from accounts.serializers import UserSerializer 
from events.models import Event
from events.serializers import EventSerializer
from sigs.models import SIG
from sigs.serializers import SIGSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_api.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.filters import UserFilter, EventFilter, SIGFilter 

class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    List all Users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsStaffOrReadOnly, 
                          IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,)
    filter_class = UserFilter

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
    permission_classes = (IsStaffOrReadOnly, 
                          IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,)

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
    permission_classes = (IsStaffOrReadOnly, 
                          permissions.IsAuthenticatedOrReadOnly,)
    filter_class = EventFilter

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
    permission_classes = (IsStaffOrReadOnly, 
                          permissions.IsAuthenticatedOrReadOnly,)

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
    permission_classes = (IsStaffOrReadOnly, 
                          permissions.IsAuthenticatedOrReadOnly,)
    filter_class = SIGFilter


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
    permission_classes = (IsStaffOrReadOnly, 
                          permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
