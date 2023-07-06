import qrcode

from db.model import Qrcodes

for i in range(1, 1001):
    data = f"https://t.me/ScanerQrCodeBot?start={i}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image()
    qr_filename = f'{i}.png'
    qr_image.save(qr_filename)
    Qrcodes().insert_into(id=i, active=False)