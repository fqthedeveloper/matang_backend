from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
def admin_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:

        return Response(
            {
                "success": False,
                "message": "Invalid username or password"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_staff:

        return Response(
            {
                "success": False,
                "message": "Admin access required"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "success": True,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username,
        "is_superuser": user.is_superuser
    })


@api_view(["GET"])
def current_admin(request):

    if not request.user.is_authenticated:

        return Response(
            {
                "authenticated": False
            }
        )

    return Response({
        "authenticated": True,
        "username": request.user.username,
        "is_superuser": request.user.is_superuser
    })