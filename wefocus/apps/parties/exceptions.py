from rest_framework import status


class InvalidParty(Exception):
    def __init__(self):
        super(InvalidParty, self).__init__('The party is over')
        self.status_code = status.HTTP_400_BAD_REQUEST


class InvalidHost(Exception):
    def __init__(self):
        super(InvalidHost, self).__init__('You are not the host of this party')
        self.status_code = status.HTTP_400_BAD_REQUEST


class InvalidMember(Exception):
    def __init__(self):
        super(InvalidMember, self).__init__('You are not part of this party')
        self.status_code = status.HTTP_400_BAD_REQUEST


class AlreadyInAParty(Exception):
    def __init__(self):
        super(AlreadyInAParty, self).__init__('You are already part of a party')
        self.status_code = status.HTTP_400_BAD_REQUEST


class PartyFull(Exception):
    def __init__(self):
        super(PartyFull, self).__init__('The party is already full')
        self.status_code = status.HTTP_400_BAD_REQUEST
