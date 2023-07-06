import os

import qrcode
from fpdf import FPDF

from db.model import Qrcodes

pdf = FPDF()

for i in range(1, 1051):
    data = f"https://t.me/ScanerQrCodeBot?start={i}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image()
    qr_filename = f'{i}.png'
    qr_image.save(qr_filename)
    pdf.add_page()
    pdf.image(qr_filename, x=10, y=10, w=190)
    Qrcodes().insert_into(id=i, active=False)
    os.remove(qr_filename)

pdf.output("qrcodes.pdf", "F")