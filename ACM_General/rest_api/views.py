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
    List all Users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        Lists all users.

        :param request: Request for UserList information.
        :type request: Request
        :rtype: Response
        :return: List of all users' details and a 200 response
                 if the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new user.

        :param request: Request to post user information.
        :type request: Request
        :rtype: Response
        :return: The newly created user's details and a 201 response
                 if the user was creates successfully, otherwise 400.
        """
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
        """
        Displays the requested user.

        :param request: Request for user information.
        :type request: Request
        :rtype: Response
        :return: The requested user's details and a 200 response
                 if the user is found, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified user.

        :param request: Request to update user information.
        :type request: Request
        :rtype: Response
        :return: The updated user's details and a 200 response if
                 successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the user from the UserList.

        :param request: Request to delete user information.
        :type request: Request
        :rtype: Response
        :return: A 204 response if successful, otherwise 404.
        """
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
        """
        Lists all Events.

        :param request: Request for EventList infomation.
        :type request: Request
        :rtype: Response
        :return: List of all Event details and a 200 response
                 if queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Event.

        :param request: Request to create new Event.
        :type request: Request
        :rtype: Response
        :return: The created event's details and a 201 response
                 if successful, otherwise 400.
        """
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
        """
        Retrieves the requested event.

        :param request: Request for Event details.
        :type request: Request
        :rtype: Response
        :return: The requested event's details and a 200 response
                 if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified event.

        :param request: Request to update Event details.
        :type request: Request
        :rtype: Response
        :return: The updated event's details and a 200 response
                 if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified event.

        :param request: Request to delete Event.
        :type request: Request
        :rtype: Response
        :return: A 204 response if successful, otherwise 404.
        """
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
        """
        Lists all SIGs' details.

        :param request: Request for SIGList details.
        :type request: Request
        :rtype: Response
        :return: The list of all SIGs and a 200 response if
                 the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a SIG.

        :param request: Request to create a SIG.
        :type request: Request
        :rtype: Response
        :return: The created SIG and a 201 response if successful,
                 otherwise 400.
        """
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
        """
        Method to retrieve the SIGSerializer class used for
        data serialization.

        :rtype: SIGSerializer.
        :return: The class used in SIGDetail's data serialization.
        """
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        """
        Retrieve the specified SIG.

        :param request: Request for SIG details.
        :type request: Request
        :rtype: Response
        :return: The specified SIG's details and a 200 response
                 if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified SIG.

        :param request: Request to update a SIG.
        :type request: Request
        :rtype: Response
        :return: The updated SIG's details and a 200 response if successful
                 otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified SIG.

        :param request: Request to delete a SIG.
        :type request: Request
        :rtype: Response
        :return: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class TransactionList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    Lists all Transactions or creates a new Transaction List.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        Lists all Transactions.

        :param request: Request for all Transaction details.
        :type request: Request
        :rtype: Response
        :return: A list of all User Transactions and a 200 response
                 if the list is non empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new User Transaction.

        :param request: Request to create a new Transaction.
        :type request: Request
        :rtype: Response
        :return: The created Transaction and a 201 response
                 if successful, otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class TransactionDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, updates, or delete a Transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieves the specified Transaction.

        :param request: Request to get Transaction details.
        :type request: Request
        :rtype: Response
        :return: The specified Transaction and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified Transaction.

        :param request: Request to update a Transaction.
        :type request: Request
        :rtype: Response
        :return: The updated Transaction and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified Transaction.

        :param request: Request to delete a Transaction.
        :type request: Request
        :rtype: Response
        :return: 204 response if succuessful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class ProductList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    List all Products or create a new Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        Retrieve the list of all Products

        :param request: Request for all Product details.
        :type request: Request
        :rtype: Response
        :return: List of all Products and a 200 response
                  if the queryset is not empty.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Product.

        :param request: Request to create a new Product.
        :type request: Request
        :rtype: Response
        :return: The created Product and a 201 response if successful,
                  otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class ProductDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, updates, or delete a Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieve the specified Product.

        :param request: Request for a Products details.
        :type request: Request
        :rtype: Response
        :return: The specified Product and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified Product.

        :param request: Request to update a Product's details.
        :type request: Request
        :rtype: Response
        :return: The updated Product and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified Product.

        :param request: Request to delete a Product.
        :type request: Request
        :rtype: Response
        :return: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)


class CategoryList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    List all Categories or create a new Category.
    """
    queryset = TransactionCategory.objects.all()
    serializer_class = CategorySerializer

    #filter_class = filters.UserFilter

    def get(self, request, *args, **kwargs):
        """
        Retrieves the list of all Categroies.

        :param request: Request for all Category details.
        :type request: Request
        :rtype: Response
        :return: List of all Categories and a 200 response if successful.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Category.

        :param request: Request to create a Category.
        :type request: Request
        :rtype: Response
        :return: The created Category's details and a 201 response
                  if successful, otherwise 400.
        """
        return self.create(request, *args, **kwargs)


class CategoryDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, updates, or delete a Category.
    """
    queryset = TransactionCategory.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieve the specified Category.

        :param request: Request to get a Category's detais.
        :type request: Request
        :rtype: Response
        :return: The specified category and a 200 response
                  if successful, otherwise 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates the specified category.

        :param request: Request to update a Category's details.
        :type: Request
        :rtype: Response
        :return: The updated category and a 200 response
                  if successful, otherwise 400.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified category.

        :param request: Request to delete a Category.
        :type: Request
        :rtype: Response
        :return: A 204 response if successful, otherwise 404.
        """
        return self.destroy(request, *args, **kwargs)

