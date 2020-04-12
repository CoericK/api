from rest_framework import serializers

from wefocus.apps.parties.models import Party, PartyMember
from wefocus.apps.timer.serializers import PomodoroTimerSerializer


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['slug', 'jitsi_id', 'host_user_id', 'member_count', 'max_member_count']


class PartyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyMember
        fields = ['user_id']
