from rest_framework import serializers

from wefocus.apps.timer.models import Timer


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ['party_id', 'focus_starts_at', 'focus_ends_at', 'break_starts_at', 'break_ends_at']
