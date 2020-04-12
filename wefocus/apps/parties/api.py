import datetime
import uuid

from .models import Party, PartyMember
from wefocus.apps.timer.models import TimerOwnerType

from wefocus.apps.timer.api import TimerManager

from .exceptions import InvalidHost, InvalidParty, InvalidMember


class PartyManger:

    def create_party(self, host_user_id):
        time = datetime.datetime.now().replace(microsecond=0)
        Party.objects.create_party(
            host_user_id=host_user_id,
            updated_at=time,
            created_at=time,
        )

    def get_party(self, user_id, party_id):
        try:
            member = PartyMember.objects.get(party_id=party_id, user_id=user_id, active=True)
        except PartyMember.DoesNotExist:
            raise InvalidMember()

        party = None
        try:
            party = Party.objects.get(id=party_id, active=True)
        except Party.DoesNotExist:
            pass

        timer = None
        members = []
        if party:
            timer_manager = TimerManager()
            timer = timer_manager.get_current_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party_id)

            members = [PartyMember.objects.filter(party_id=party_id, active=True)]


        return None  # the view

    def _validate_party_and_host(self, user_id, party_id):
        try:
            party = Party.objects.get(id=party_id, active=True)
        except Party.DoesNotExist:
            raise InvalidParty()

        if party.host_user_id != user_id:
            raise InvalidHost()

    def start_pomodoro_timer(self, user_id, party_id):
        self._validate_party_and_host(user_id=user_id, party_id=party_id)

        timer_manager = TimerManager()
        timer = timer_manager.start_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party_id)

        return None  # return the party view

    def end_pomodoro_timer(self, user_id, party_id):
        self._validate_party_and_host(user_id=user_id, party_id=party_id)

        timer_manager = TimerManager()
        timer = timer_manager.end_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party_id)

        return None  # return the party view