from db.model import QrCode

for i in range(1, 10051):
    QrCode().create(active=False)
