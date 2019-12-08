from rest_framework import generics

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user view
    """
    serializer_class = UserSerializer
