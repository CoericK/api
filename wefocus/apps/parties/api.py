import datetime
import uuid

from .models import Party, PartyMember, PartyMemberRole
from wefocus.apps.timer.models import TimerOwnerType

from wefocus.apps.timer.api import TimerManager

from .exceptions import InvalidHost, InvalidParty, InvalidMember, AlreadyInAParty, PartyFull


class PartyManger:

    def create_party(self, host_user_id):
        if PartyMember.objects.filter(user_id=user_id, active=True).count() > 0:
            raise AlreadyInAParty()

        time = datetime.datetime.now().replace(microsecond=0)
        party = Party.objects.create_party(
            host_user_id=host_user_id,
            updated_at=time,
            created_at=time,
        )

        return self.get_party_view(user_id=host_user_id, party_slug=party.slug)

    def get_party_view(self, user_id, party_slug, party=None):
        party = party or self._get_party_safe(party_slug=party_slug)

        try:
            PartyMember.objects.get(party_id=party.id, user_id=user_id, active=True)
        except PartyMember.DoesNotExist:
            raise InvalidMember()

        timer = None
        members = []
        if party:
            timer_manager = TimerManager()
            timer = timer_manager.get_current_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party.id)

            members = [PartyMember.objects.filter(party_id=party.id, active=True)]

        return None  # the view

    def join_party(self, user_id, party_slug):
        party = self._validate_party(party_slug=party_slug)
        current_time = datetime.datetime.now().replace(microsecond=0)

        # TODO: atomic lock on party
        active_members_of_this_party = PartyMember.objects.filter(party_id=party, active=True)
        if active_members_of_this_party.count() >= party.max_member_count:
            raise PartyFull()

        active_members_of_this_user = PartyMember.objects.filter(user_id=user_id, active=True)
        for member in active_members_of_this_user:
            if member.party_id == party.id:
                if member.last_left_at is None:
                    # user is trying to join a party the user is already actively in.
                    # probably the user accidentally got disconnected or trying to connect from more than one browser
                    # Let it go through for now.
                    pass
                else:
                    # user is trying to rejoin the party
                    member.last_joined_at = current_time
                    member.save()

                return self.get_party_view(user_id=user_id, party_slug=party_slug)
            elif member.last_left_at is None:
                raise AlreadyInAParty()

        PartyMember.objects.create_member(party_id=party.id, user_id=user_id,
                                          role=PartyMemberRole.USER, last_joined_at=current_time)

        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party)

    def leave_party(self, user_id, party_slug):
        party = self._validate_party(party_slug=party_slug)
        current_time = datetime.datetime.now().replace(microsecond=0)

        # TODO: atomic lock on party
        try:
            member = PartyMember.objects.get(party_id=party_id, user_id=user_id, active=True)
        except PartyMember.DoesNotExist:
            raise InvalidMember()

        if member.last_left_at > member.last_joined_at:
            raise InvalidMember()

        member.last_left_at = current_time
        member.save()

        if member.user_id == party.host_user_id:
            Party.objects.discard(party_id=party.id)

        # client will not render the party UI if the party member list in the response does not include the user
        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party)

    def start_pomodoro_timer(self, user_id, party_slug):
        party = self._validate_party_and_host(user_id=user_id, party_slug=party_slug)

        # TODO: atomic lock on party
        timer_manager = TimerManager()
        timer = timer_manager.start_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party.id)

        return None  # return the party view

    def end_pomodoro_timer(self, user_id, party_slug):
        party = self._validate_party_and_host(user_id=user_id, party_slug=party_slug)

        # TODO: atomic lock on party
        timer_manager = TimerManager()
        timer = timer_manager.end_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party.id)

        return None  # return the party view

    ##################################################
    # Internal methods
    ##################################################

    def _get_party_safe(self, party_slug):
        party = None
        try:
            party = Party.objects.get(slug=party_slug, active=True)
        except Party.DoesNotExist:
            pass

        return party

    def _validate_party(self, party_slug):
        party = self._get_party_safe(party_slug=party_slug)
        if not party:
            raise InvalidParty()

        return party

    def _validate_party_and_host(self, user_id, party_slug):
        party = self._validate_party(party_slug=party_slug)

        if party.host_user_id != user_id:
            raise InvalidHost()

        return party
