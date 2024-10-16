from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import decorators
from rest_framework.authtoken.models import Token

from .models import User


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("username")
    password = request.data.get("password")
    user = User.objects.filter(username=username)
    if not user:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    user = user.first()
    
    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "405",
            "data": None
        })
    token = Token.objects.get_or_create(user=user)
    return Response({
        "status": "success",
        "code": "200",
        "data": token[0].__str__(),
    })
