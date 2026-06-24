from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.views.common_serializers import InvitationTokenBaseSerializer
from ies.models import User, InvitationToken
from api.views.ies.serializers import (
    InstitutionFullSerializer, InstitutionSimpleSerializer)


class UserLoginSerializer(serializers.Serializer):
    """Login por email o username; ambos llegan en el campo `email`."""

    email = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})

    def validate_email(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Campo requerido.')
        return value


class UserDataSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField(source="full_name")
    token = serializers.ReadOnlyField(source="auth_token.key")
    institution = InstitutionSimpleSerializer(read_only=True)
    institution_details = InstitutionFullSerializer(
        read_only=True, source="institution")
    is_ies = serializers.SerializerMethodField()
    is_reviewer = serializers.ReadOnlyField(source="reviewer")

    def get_is_ies(self, obj):
        return obj.institution is not None

    class Meta(object):
        model = User
        fields = [
            "id", 'email', 'username', "first_name", "last_name",
            "token", "fullname", "reviewer", "is_staff",
            "is_superuser", "institution", "institution_details",
            "is_ies", "is_reviewer"]


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_staff",
            "is_superuser",
            "first_name",
            "last_name",
            "reviewer",
            "full_name",
        ]


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8,
        style={ 'input_type': 'password' })
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    checkCondiction = serializers.BooleanField(
        required=False)
    key = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined"
        ]
        # read_only_fields = [
        #     "last_login",
        #     "is_superuser",
        #     "username",
        #     "full_name",
        #     "is_staff",
        #     "is_active",
        #     "date_joined"
        # ]


class UserRegistrationSerializer(UserDataSerializer):

    class Meta:
        model = User
        fields = UserDataSerializer.Meta.fields + ["password"]
        # read_only_fields = UserDataSerializer.Meta.read_only_fields


class PasswordRecoveryRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value.strip().lower()


class InvitationTokenCheckSerializer(serializers.ModelSerializer):
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')

    class Meta:
        model = InvitationToken
        fields = ["email", "institution", "institution_full"]


class InvitationTokenListSerializer(InvitationTokenBaseSerializer):
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')

    class Meta:
        model = InvitationToken
        fields = InvitationTokenBaseSerializer.Meta.fields + ['institution_full']


class InvitationTokenCreateSerializer(InvitationTokenListSerializer):

    def validate(self, data):
        institution = data.get('institution')
        email = data.get('email')
        if not institution and not email:
            raise serializers.ValidationError({
                'email': (
                    'El email es obligatorio cuando no se '
                    'asocia una institución.'
                )
            })
        if not institution:
            request = self.context.get('request')
            user = getattr(request, 'user', None)
            if not user or not user.is_superuser:
                raise serializers.ValidationError({
                    'detail': (
                        'Solo una persona superusuaria puede crear '
                        'invitaciones sin institución.'
                    )
                })
        return data


class UserListSerializer(serializers.ModelSerializer):
    """Listado de personas usuarias para el panel de gestión de la
    superusuaria. Excluye campos sensibles (password, auth token) y
    expone las banderas de permisos que el panel puede alternar.
    """

    fullname = serializers.ReadOnlyField(source='full_name')

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'fullname', 'is_active', 'reviewer', 'is_staff',
            'is_superuser', 'last_login', 'date_joined',
        ]
        read_only_fields = fields


class UserPermissionsUpdateSerializer(serializers.ModelSerializer):
    """Restringe el PATCH a nombre y banderas de permisos.

    Una persona superusuaria no puede modificarse a sí misma desde
    este endpoint — esto evita un lockout accidental (quitarse
    `is_superuser` o `is_active`) y obliga a usar el endpoint de
    perfil propio para editar nombre.
    """

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'is_active', 'reviewer',
            'is_staff', 'is_superuser',
        ]

    def validate(self, data):
        request = self.context.get('request')
        actor = getattr(request, 'user', None)
        if actor and self.instance and actor.pk == self.instance.pk:
            raise serializers.ValidationError({
                'detail': (
                    'No puedes modificar tus propios datos desde '
                    'este endpoint.'
                )
            })
        return data

    def to_representation(self, instance):
        return UserListSerializer(
            instance, context=self.context).data


class InvitationTokenDetailSerializer(InvitationTokenListSerializer):
    class Meta(InvitationTokenListSerializer.Meta):
        pass


class PasswordRecoveryConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        if data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': (
                    'Las contraseñas no coinciden.'
                ),
            })
        return data


class UserRegistrationFromInvitationSerializer(
    PasswordRecoveryConfirmSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Ya existe una persona usuaria registrada con este correo.'
            )
        return value.lower()
