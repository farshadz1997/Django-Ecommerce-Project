from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import AddressSerializer
from ..models import Address


class AuthenticateUserAPI(ObtainAuthToken):
    """
    This class is used to authenticate user and generate token.
    """

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "email": user.email})


class AddressesAPI(APIView):
    """
    This API is used to get user addresses.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get(self, request):
        addresses = request.user.addresses.all()
        serializer = self.serializer_class(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressAPI(RetrieveUpdateDestroyAPIView):
    """
    This API is used to get, update, delete user address.
    """

    authentication_class = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.request.user.addresses.all()


class CreateAddressAPI(CreateAPIView):
    """
    This API is used to create new address.
    """

    authentication_class = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def post(self, request):
        if Address.objects.filter(customer=self.request.user).count() == 4:
            return Response({"error": "You can't have more than 4 addresses."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        country_code = serializer.validated_data["country"]
        if Address.objects.filter(customer=self.request.user, default=True).count() == 0:
            serializer.save(customer=request.user, country=country_code, default=True)
        else:
            serializer.save(customer=request.user, country=country_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
