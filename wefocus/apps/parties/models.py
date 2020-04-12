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
                                          role=PartyMemberRole.HOST, last_joined_at=created_at)
        return party

    def discard(self, party_id):
        PartyMember.objects.filter(active=True, party_id=party_id).update(active=False)
        PomodoroTimer.objects.filter(active=True, wner_type=TimerOwnerType.PARTY, owner_id=party_id)\
                             .update(active=False)
        self.filter(id=party_id).update(active=False)


class Party(models.Model):
    jitsi_id = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=200)
    host_user_id = models.IntegerField()

    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    member_count = models.IntegerField(default=1)
    max_member_count = models.IntegerField(default=6)   # TODO: get from a config value

    active = models.BooleanField(default=True)

    objects = PartyManager()

    class Meta:
        verbose_name_plural = 'parties'
        unique_together = ['jitsi_id',
                           'slug']
        index_together = [['active', 'host_user_id'],
                          ['active', 'member_count', 'max_member_count']]


class PartyMemberManager(models.Manager):

    def create_member(self, party_id, user_id, role, last_joined_at):
        member = self.create(party_id=party_id, user_id=user_id, role=role, last_joined_at=last_joined_at)
        return member


class PartyMember(models.Model):
    party_id = models.IntegerField()
    user_id = models.IntegerField()

    role = models.IntegerField()

    last_joined_at = models.DateTimeField()
    last_left_at = models.DateTimeField(default=None, null=True)

    active = models.BooleanField(default=True)

    objects = PartyMemberManager()

    class Meta:
        verbose_name_plural = 'party_members'
        unique_together = [['active', 'party_id', 'user_id']]
        index_together = [['user_id', 'active']]

