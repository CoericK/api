from rest_framework import serializers

from wefocus.users.models import User
from wefocus.apps.parties.models import PartyMember


class UserSerializer(serializers.ModelSerializer):
    party_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'url', 'party_id']

        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', 'lookup_field': 'username'}
        }

    def get_party_id(self, obj):
        party_member_query = PartyMember.objects.filter(active=True)
        if party_member_query.exists():
            return party_member_query.first().party_id
        else:
            None
