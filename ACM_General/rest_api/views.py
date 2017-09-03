from accounts.models import User
from accounts.serializers import UserSerializer
from events.models import Event
from events.serializers import EventSerializer
from payments.models import Transaction, Product, TransactionCategory
from payments.serializers import TransactionSerializer, ProductSerializer, CategorySerializer
from sigs.models import SIG
from sigs.serializers import SIGSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
# from rest_api.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import filters


class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    @Desc: List all Users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Lists all users.

        @Returns: List of all users' details and a 200 response
                  if the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a new user.

        @Returns: The newly created user's details and a 201 response
                  if the user was creates successfully, otherwise 400.
        """ 
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        @Desc: Displays the requested user.

        @Returns: The requested user's details and a 200 response
                  if the user is found, otherwise 404. 
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified user.

        @Returns: The updated user's details and a 200 response if
                  successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the user from the UserList.

        @Returns: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class EventList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    @Desc: List all Events or create a new event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = filters.EventFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Lists all Events.

        @Returns: List of all Event details and a 200 response
                  if queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a new Event.

        @Returns: The created event's details and a 201 response 
                  if successful, otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class EventDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a Event instance.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieves the requested event.
        
        @Returns: The requested event's details and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified event.

        @Returns: The updated event's details and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the specified event.

        @Returns: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class SIGList(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              generics.GenericAPIView):
    """
    @Desc: List all SIGs or create a new sig.
    """
    queryset = SIG.objects.all()
    serializer_class = SIGSerializer
    filter_class = filters.SIGFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Lists all SIGs' details.

        @Returns: The list of all SIGs and a 200 response if
                  the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a SIG.

        @Returns: The created SIG and a 201 response if successful, 
                  otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class SIGDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a SIG instance.
    """
    queryset = SIG.objects.all()
    serializer_class = SIGSerializer

    def get_serializer_class(self):
        """
        @Desc: Method to retrieve the SIGSerializer class used for 
               data serialization.

        @Returns: The class used in SIGDetail's data serialization.
        """ 
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieve the specified SIG.

        @Returns: The specified SIG's details and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified SIG.

        @Returns: The updated SIG's details and a 200 response if successful
                  otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the specified SIG.

        @Returns: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class TransactionList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    @Desc: Lists all Transactions or creates a new Transaction List.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Lists all Transactions.

        @Returns: A list of all User Transactions and a 200 response
                  if the list is non empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a new User Transaction.

        @Returns: The created Transaction and a 201 response 
                  if successful, otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class TransactionDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a Transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieves the specified Transaction.

        @Returns: The specified Transaction and a 200 response 
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified Transaction.

        @Returns: The updated Transaction and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the specified Transaction.

        @Returns: 204 response if succuessful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class ProductList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    @Desc: List all Products or create a new Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieve the list of all Products

        @Returns: List of all Products and a 200 response
                  if the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a new Product.

        @Returns: The created Product and a 201 response if successful,
                  otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class ProductDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieve the specified Product.

        @Returns: The specified Product and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified Product.

        @Returns: The updated Product and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the specified Product.

        @Returns: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class CategoryList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    @Desc: List all Categories or create a new Category.
    """
    queryset = TransactionCategory.objects.all()
    serializer_class = CategorySerializer

    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieves the list of all Categroies.

        @Returns: List of all Categories and a 200 response if successful.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        @Desc: Creates a new Category.

        @Returns: The created Category's details and a 201 response
                  if successful, otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class CategoryDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    @Desc: Retrieve, updates, or delete a Category.
    """
    queryset = TransactionCategory.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        """
        @Desc: Retrieve the specified Category.

        @Returns: The specified category and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        @Desc: Updates the specified category.

        @Returns: The updated category and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        @Desc: Deletes the specified category.

        @Returns: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)

