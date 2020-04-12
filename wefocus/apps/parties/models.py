from django.db import models
from wefocus.users.models import User
from wefocus.apps.timer.models import PomodoroTimer, TimerOwnerType
import uuid


class PartyMemberRole:
    HOST = 0
    MEMBER = 1


class PartyManager(models.Manager):

    def create_party(self, host_user_id, created_at, slug=uuid.uuid4()):
        party = self.create(slug=slug, host_user_id=host_user_id,
                            updated_at=created_at, created_at=created_at)
        PartyMember.objects.create_member(party_id=party.id, user_id=host_user_id,
                                          role=PartyMemberRole.HOST, joined_at=created_at)
        return party

    def discard(self, party_id):
        self.filter(id=party_id).update(active=False)
        PartyMember.objects.filter(active=True, party_id=party_id).update(active=False)
        PomodoroTimer.objects.filter(active=True, wner_type=TimerOwnerType.PARTY, owner_id=party_id)\
                             .update(active=False)


class Party(models.Model):
    jitsi_id = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=200)
    host_user_id = models.IntegerField()

    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    active = models.BooleanField(default=True)

    objects = PartyManager()

    class Meta:
        verbose_name_plural = 'parties'
        unique_together = ['jitsi_id', 'slug']


class PartyMemberManager(models.Manager):

    def create_member(self, party_id, user_id, role, joined_at):
        member = self.create(party_id=party_id, user_id=user_id, role=role, joined_at=joined_at)
        return member


class PartyMember(models.Model):
    party_id = models.IntegerField()
    user_id = models.IntegerField()

    role = models.IntegerField()

    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(default=None)

    active = models.BooleanField(default=True)

    objects = PartyMemberManager()

    class Meta:
        verbose_name_plural = 'party_members'
        unique_together = ['active', 'party_id', 'user_id']

