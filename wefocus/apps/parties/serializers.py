from rest_framework import serializers

from wefocus.apps.parties.models import Party


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['slug', 'jitsi_id']

        # extra_kwargs = {
        #     'url': {'view_name': 'api:party-detail', 'lookup_field': 'uuid'}
        # }
