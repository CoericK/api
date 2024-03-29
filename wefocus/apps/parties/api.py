import datetime
import uuid

from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from .models import Party, PartyMember, PartyMemberRole
from wefocus.apps.timer.models import TimerOwnerType

from wefocus.apps.timer.api import TimerManager

from .exceptions import InvalidHost, InvalidParty, InvalidMember, AlreadyInAParty, PartyFull
from .serializers import PartyViewSerializer


from .serializers import PartySerializer, PartyMemberSerializer
from wefocus.apps.timer.serializers import PomodoroTimerSerializer


class PartyManger:

    def create_party(self, host_user_id):
        if PartyMember.objects.filter(user_id=host_user_id, active=True).count() > 0:
            raise AlreadyInAParty()

        time = datetime.datetime.now().replace(microsecond=0)
        party = Party.objects.create_party(
            host_user_id=host_user_id,
            created_at=time,
        )

        return self.get_party_view(user_id=host_user_id, party_slug=party.slug)

    def get_party_view(self, user_id, party_slug, party=None, timer=None, shallow=False):
        party = party or self._get_party_safe(party_slug=party_slug)

        # if party:
        #     try:
        #         PartyMember.objects.get(party_id=party.id, user_id=user_id, active=True)
        #     except PartyMember.DoesNotExist:
        #         party = None

        members = None
        if not shallow and party:
            timer_manager = TimerManager()
            timer = timer or timer_manager.get_current_pomodoro_timer(owner_type=TimerOwnerType.PARTY,
                                                                      owner_id=party.id)

            members = PartyMember.objects.filter(party_id=party.id, active=True)

        response_data = {
            'party': PartySerializer(party).data,
            'timer': PomodoroTimerSerializer(timer).data,
            'members': PartyMemberSerializer(members, many=True).data,
        }

        return Response(status=status.HTTP_200_OK, data=response_data)

    def get_parties(self):
        parties = Party.objects.filter(active=True, member_count__lt=F('max_member_count'))[:50]  # TODO: get from config
        parties_view = PartySerializer(parties, many=True)

        response_data = {
            'parties': parties_view.data,
        }

        return Response(status=status.HTTP_200_OK, data=response_data)

    def join_party(self, user_id, party_slug):
        party = self._validate_party(party_slug=party_slug)
        current_time = datetime.datetime.now().replace(microsecond=0)

        # TODO: atomic lock on party
        if party.member_count >= party.max_member_count:
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
        party.member_count += 1
        party.save()

        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party)

    def leave_party(self, user_id, party_slug):
        party = self._validate_party(party_slug=party_slug)
        current_time = datetime.datetime.now().replace(microsecond=0)

        # # TODO: atomic lock on party
        # try:
        #     member = PartyMember.objects.get(party_id=party.id, user_id=user_id, active=True)
        # except PartyMember.DoesNotExist:
        #     raise InvalidMember()

        members = PartyMember.objects.filter(party_id=party.id, user_id=user_id, active=True)
        for member in members:
            if member.last_left_at is not None and member.last_left_at > member.last_joined_at:
                raise InvalidMember()

            member.last_left_at = current_time
            member.save()

            if member.user_id == party.host_user_id:
                Party.objects.discard(party_id=party.id)
            else:
                party.member_count -= 1
                party.save()

        # client will not render the party UI if the party member list in the response does not include the user
        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party)

    def delete_party(self, party_slug):
        # TEMPORARY METHOD
        party_ids = [Party.objects.filter(slug=party_slug).values_list('id', flat=True)]
        Party.objects.filter(slug=party_slug).update(active=False)
        PartyMember.objects.filter(party_id__in=party_ids).update(active=False)
        from wefocus.apps.timer.models import PomodoroTimer
        PomodoroTimer.objects.filter(owner_id__in=party_ids).update(active=False)
        return Response(status=status.HTTP_200_OK, data='1')

    def start_pomodoro_timer(self, user_id, party_slug, focus_duration, break_duration):
        party = self._validate_party_and_host(user_id=user_id, party_slug=party_slug)
        current_time = datetime.datetime.now().replace(microsecond=0)
        focus_starts_at = current_time
        focus_ends_at = focus_starts_at + datetime.timedelta(minutes=focus_duration)
        break_starts_at = focus_ends_at
        break_ends_at = break_starts_at + datetime.timedelta(minutes=break_duration)

        # TODO: atomic lock on party
        timer_manager = TimerManager()
        timer = timer_manager.start_pomodoro_timer(
            owner_type=TimerOwnerType.PARTY, owner_id=party.id,
            focus_starts_at=focus_starts_at, focus_ends_at=focus_ends_at,
            break_starts_at=break_starts_at, break_ends_at=break_ends_at)

        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party, timer=timer)

    def restart_pomodoro_timer(self, user_id, party_slug, focus_duration, break_duration):
        self.end_pomodoro_timer(user_id=user_id, party_slug=party_slug)
        return self.start_pomodoro_timer(user_id=user_id, party_slug=party_slug,
                                         focus_duration=focus_duration, break_duration=break_duration)

    def end_pomodoro_timer(self, user_id, party_slug):
        party = self._validate_party_and_host(user_id=user_id, party_slug=party_slug)

        # TODO: atomic lock on party
        timer_manager = TimerManager()
        timer_manager.end_pomodoro_timer(owner_type=TimerOwnerType.PARTY, owner_id=party.id)

        return self.get_party_view(user_id=user_id, party_slug=party_slug, party=party)

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
