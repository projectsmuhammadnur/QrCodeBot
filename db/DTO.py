class QrCodesDto:
    def __init__(self,
                 id: int = None,
                 active: bool = False
                 ):
        self.id = id
        self.active = active


class UsersDto:
    def __init__(self,
                 id: int = None,
                 user_id: str = None,
                 name: str = None,
                 phone: str = None,
                 qrcode_id: int = None,
                 created_at: str = None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.qrcode_id = qrcode_id
        self.created_at = created_at
