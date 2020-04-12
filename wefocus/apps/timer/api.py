from .models import PomodoroTimer
from .exceptions import TimerStartedException

import logging


class TimerManager:

    def start_pomodoro_timer(self, owner_type, owner_id, focus_starts_at, focus_ends_at,
                             break_starts_at, break_ends_at):
        if PomodoroTimer.objects.filter(owner_type=owner_type, owner_id=owner_id, active=True).count() > 0:
            raise TimerStartedException()

        timer = PomodoroTimer.objects.create_timer(
            owner_type=owner_type,
            owner_id=owner_id,
            focus_starts_at=focus_starts_at,
            focus_ends_at=focus_ends_at,
            break_starts_at=break_starts_at,
            break_ends_at=break_ends_at
        )

        return timer

    def get_current_pomodoro_timer(self, owner_type, owner_id):
        timer = None

        try:
            timer = PomodoroTimer.objects.get(owner_type=owner_type, owner_id=owner_id, active=True)
        except PomodoroTimer.DoesNotExist:
            logging.error('get_current_pomodoro_timer - timer does not exist - (%s, %s)' % (owner_type, owner_id))
            pass

        return timer

    def end_pomodoro_timer(self, owner_type, owner_id):
        timer = self.get_current_pomodoro_timer(owner_type=owner_type, owner_id=owner_id)
        if timer:
            PomodoroTimer.objects.discard(id=timer.id)

        return timer
