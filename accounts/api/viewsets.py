from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Address
from .serializers import (AddressSerializer, ChangePasswordSerializer,
                          RegisterAccountSerializer, UpdateAccountSerializer)
from orders.api.serializers import OrderSerializer
from orders.models import Order


class RegisterAPI(APIView):
    """
    This API is used to register users
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({"email": serializer.validated_data["email"]}, status=status.HTTP_201_CREATED)


class AuthenticateUserAPI(ObtainAuthToken):
    """
    This API is used to authenticate user and generate token.
    """

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        response =  Response({"token": token.key, "email": user.email})
        response.set_cookie("Authorization", f"Token {token.key}")
        return response


class LogoutAPI(APIView):
    """
    This API is used to logout the user and clear the session
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.session.clear()
        request.user.auth_token.delete()
        response = Response("You have been loged out", status=status.HTTP_200_OK)
        response.delete_cookie("Authorization")
        return response
 
    
class ChangePasswordAPI(APIView):
    """
    This API is used to change password
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
    
class UpdateUserAPI(APIView):
    """
    This API is used to update user details
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateAccountSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressesAPI(APIView):
    """
    This API is used to get all user addresses.
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


class UserOrdersAPI(APIView):
    """This API return all of the user orders"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user, billing_status=True)
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    