from rest_framework import serializers

from ies.models import InvitationToken, User


class UserSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class InvitationTokenBaseSerializer(serializers.ModelSerializer):
    destination_url = serializers.SerializerMethodField()
    user = UserSimpleSerializer(read_only=True)

    def get_destination_url(self, obj):
        from api.views.auth.common_utils import get_destination_url
        return get_destination_url(obj, 'register')

    class Meta:
        model = InvitationToken
        fields = [
            'key', 'email', 'institution',
            'created_at', 'viewed_at', 'used_at',
            'reviewer', 'is_staff', 'is_superuser',
            'destination_url', 'email_sent', 'user',
        ]
