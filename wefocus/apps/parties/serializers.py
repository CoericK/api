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


# class PartyResponseSerializer(serializers.Serializer):
#     party = PartySerializer(read_only=True)
#     pomodoro_timer = PomodoroTimerSerializer(read_only=True)
#     members = PartyMemberSerializer(ready_only=True, many=True)



