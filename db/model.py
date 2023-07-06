from db.config import DB


class Qrcodes(DB):
    def __init__(self, *fields):
        self.fields = fields


class Users(DB):
    def __init__(self, *fields):
        self.fields = fields