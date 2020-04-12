class InvalidParty(Exception):
    def __init__(self):
        super(InvalidParty, self).__init__('The party is over')
        self.status_code = 400  # check if this works


class InvalidHost(Exception):
    def __init__(self):
        super(InvalidHost, self).__init__('You are not the host of this party')
        self.status_code = 400  # check if this works


class InvalidMember(Exception):
    def __init__(self):
        super(InvalidMember, self).__init__('You are not part of this party')
        self.status_code = 400  # check if this works
