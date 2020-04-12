from django.db import models
from wefocus.users.models import User
import uuid


class PartyManager(models.Manager):
    def create_party(self, host_user_id, updated_at, created_at, slug=uuid.uuid4()):
        self.create(
            slug=slug,
            host_user_id=host_user_id,
            updated_at=updated_at,
            created_at=created_at,
        )

    def discard(self, party_id):
        self.filter(id=party_id).update(active=False)


class Party(models.Model):
    jitsi_id = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=200)
    host_user_id = models.IntegerField()
    active = models.BooleanField(default=True)

    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    objects = PartyManager()

    class Meta:
        verbose_name_plural = 'parties'
        unique_together = ['jitsi_id', 'slug']

