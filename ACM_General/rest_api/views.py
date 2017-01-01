from accounts.models import User 
from accounts.serializers import UserSerializer 
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_api.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly

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
