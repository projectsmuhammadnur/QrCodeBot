from db.model import Qrcodes

for i in range(1, 10051):
    Qrcodes().insert_into(id=i, active=False)