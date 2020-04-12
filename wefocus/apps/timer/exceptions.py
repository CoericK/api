from rest_framework import status


class TimerStartedException(Exception):
    def __init__(self):
        super(TimerStartedException, self).__init__('Timer already exists. End the timer before starting a new one.')
        self.status_code = status.HTTP_400_BAD_REQUEST
