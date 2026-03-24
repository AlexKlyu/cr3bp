"""Generate styled QR codes for the project."""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os

OUT = os.path.dirname(os.path.abspath(__file__))

codes = {
    'qr_main.png': 'https://rocketlauncher.space',
    'qr_simulator.png': 'https://rocketlauncher.space/simulator.html',
}

for filename, url in codes.items():
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=30, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    path = os.path.join(OUT, filename)
    img.save(path)
    print(f"Saved: {path} ({img.size[0]}x{img.size[1]})")
