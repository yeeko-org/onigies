from django.db.models import Q
from rest_framework import permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException, ParseError
from rest_framework.request import Request
from rest_framework.response import Response

from api.views.auth import serializers
from ies.models import User


class UserLoginAPIView(views.APIView):
    """Login por email o username (ambos llegan en el campo `email`)."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request: Request) -> Response:
        """Autentica al usuario y devuelve sus datos junto al token."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user_query = User.objects\
            .filter(username=identifier)\
            .select_related('institution', 'auth_token')
        if not user_query.exists():
            user_query = User.objects\
                .filter(email=identifier)\
                .select_related('institution', 'auth_token')

        count = user_query.count()
        if count == 0:
            raise ParseError(detail='Usuario o correo no válido.')
        if count > 1:
            msg = (
                'Existen múltiples usuarios con ese identificador. '
                'Contacta al administrador.')
            raise APIException(detail=msg)

        user_obj = user_query.first()
        if not user_obj.check_password(password):
            raise ParseError(detail='Credenciales inválidas.')
        if not user_obj.is_active:
            raise ParseError(detail='Usuario no activo.')

        user_obj.auth_token, _ = Token.objects.get_or_create(user=user_obj)

        user_serializer = serializers.UserDataSerializer(
            user_obj, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        """Devuelve los datos del usuario autenticado en sesión."""
        user = request.user
        if user.is_authenticated:
            user_serializer = serializers.UserDataSerializer(
                user, context={'request': request})
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response()

