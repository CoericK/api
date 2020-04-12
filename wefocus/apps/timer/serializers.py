from rest_framework import serializers

from wefocus.apps.timer.models import PomodoroTimer


class PomodoroTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroTimer
        fields = ['owner_id', 'focus_starts_at', 'focus_ends_at', 'break_starts_at', 'break_ends_at']
