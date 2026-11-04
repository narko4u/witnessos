#!/usr/bin/env python3
"""Generate a printable VoltLedger installation QR once an HTTPS pilot URL exists.

Usage:
  python3 make_install_qr.py https://approved.example/voltledger/
Requirements:
  python3 -m pip install qrcode
No network access or data upload. QR contains only the provided URL.
"""
import argparse
import html
from pathlib import Path
from urllib.parse import urlsplit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Approved HTTPS URL of the deployed PWA")
    parser.add_argument("--out", default="voltledger-install", help="Output filename prefix")
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        parser.error("Use a fully qualified HTTPS app URL without embedded credentials.")
    try:
        import qrcode
        from qrcode.image.svg import SvgPathImage
    except ImportError:
        parser.error("Install the free 'qrcode' Python package first.")
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(args.url)
    qr.make(fit=True)
    path = Path(args.out)
    svg = path.with_suffix(".svg")
    svg.write_bytes(qr.make_image(image_factory=SvgPathImage).to_string())
    card = path.with_suffix(".html")
    url = html.escape(args.url, quote=True)
    card.write_text(
        f'<!doctype html><html lang="en-AU"><meta charset="utf-8">'
        f'<title>VoltLedger install card</title><style>'
        f'body{{margin:5vh auto;max-width:520px;text-align:center;background:#080b0a;color:#efefef;'
        f'font:17px system-ui}}img{{max-width:80%;background:white;padding:18px;border-radius:14px}}'
        f'h1{{color:#c9a84c}}p{{padding:0 25px}}small{{overflow-wrap:anywhere}}</style>'
        f'<h1>VOLTLEDGER</h1><p>Scan to open your field register.</p>'
        f'<img src="{html.escape(svg.name, quote=True)}" alt="VoltLedger installation QR code">'
        f'<p>Open in your phone browser, then choose Install app or Add to Home Screen.</p>'
        f'<small>{url}</small><p><small>Requires an approved HTTPS pilot deployment. '
        f'QR links to software; it does not pair to a tester.</small></p></html>',
        encoding="utf-8",
    )
    print(f"Created {svg} and {card}. Verify the QR with a separate phone before distribution.")

if __name__ == "__main__":
    main()
