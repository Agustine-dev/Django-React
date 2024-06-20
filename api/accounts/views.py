
from django.contrib.auth import authenticate
from rest_framework import generics, views
from rest_framework.response import Response
from .serializers import UserSerializer
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse

class LoginView(views.APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user:
            # update response
            try:
                if user.auth_token:
                    return Response({"token":user.auth_token.key }, status=200)
            except:
                return Response({"error": "Auth Incomplete,Contact Admin"}, status=305)

            return Response({"token": user.auth_token.key }, status=200)
        else:
            return Response({"error": "Wrong Credentials"}
            ,status=400)

class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    # Exempt UserCreate from global auth scheme
    authentication_classes = ()
    permission_classes = ()


