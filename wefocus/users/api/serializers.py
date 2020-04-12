from rest_framework import serializers

from wefocus.users.models import User
from wefocus.apps.parties.models import Party, PartyMember


class UserSerializer(serializers.ModelSerializer):
    party_slug = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'url', 'party_slug']

        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', 'lookup_field': 'username'}
        }

    def get_party_slug(self, obj):
        party_member_query = PartyMember.objects.filter(active=True)
        if party_member_query.exists():
            try:
                return Party.objects.get(id=party_member_query.first().party_id).slug
            except Party.DoesNotExist:
                return None
        else:
            return None
