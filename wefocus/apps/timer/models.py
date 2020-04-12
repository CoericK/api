from django.db import models


class TimerOwnerType:
    PARTY = 1


class BaseTimerManager(models.Manager):

    def discard(self, timer_id):
        self.filter(id=timer_id).update(active=False)


class BaseTimer(models.Model):
    owner_type = models.IntegerField()
    owner_id = models.IntegerField()

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'timers'


class PomodoroTimerManager(BaseTimerManager):

    def create_timer(self, owner_type, owner_id, focus_starts_at, focus_ends_at, break_starts_at, break_ends_at):
        timer = self.create(
            owner_type=owner_type,
            owner_id=owner_id,
            focus_starts_at=focus_starts_at,
            focus_ends_at=focus_ends_at,
            break_starts_at=break_starts_at,
            break_ends_at=break_ends_at,
        )

        return timer


class PomodoroTimer(BaseTimer):
    focus_starts_at = models.IntegerField()
    focus_ends_at = models.IntegerField()

    break_starts_at = models.IntegerField()
    break_ends_at = models.IntegerField()

    objects = PomodoroTimerManager()

    class Meta:
        verbose_name_plural = 'pomodoro_timers'
        index_together = ['active', 'owner_type', 'owner_id', 'focus_starts_at']
