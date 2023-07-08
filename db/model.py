from db.config import QrcodeDAO, UserDAO


class Qrcodes(QrcodeDAO):
    def __init__(self, *fields):
        self.fields = fields


class Users(UserDAO):
    def __init__(self, *fields):
        self.fields = fields