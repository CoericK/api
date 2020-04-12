import datetime
import uuid

from .models import Party
from wefocus.apps.timer.models import TimerOwnerType

from wefocus.apps.timer.api import TimerManager


class PartyManger:
    def create_party(self, host_user_id):
        time = datetime.datetime.now().replace(microsecond=0)
        Party.objects.create_party(
            host_user_id=host_user_id,
            updated_at=time,
            created_at=time,
        )

    def start_pomodoro_timer(self, user_id, party_id):
        timer_manager = TimerManager()
        timer = timer_manager.start_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party_id)

        return None  # return the party view
