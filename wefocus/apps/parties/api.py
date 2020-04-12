import datetime
import uuid

from .models import Party


class PartyManger:
    def create_party(self, host_user_id):
        time = datetime.datetime.now().replace(microsecond=0)
        Party.objects.create_party(
            host_user_id=host_user_id,
            updated_at=time,
            created_at=time,
        )
