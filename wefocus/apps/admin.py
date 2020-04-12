from django.contrib import admin

from .parties.models import Party, PartyMember
from .timer.models import PomodoroTimer

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'jitsi_id')
    search_fields = ['slug']
