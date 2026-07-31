import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import json
from urllib.parse import urlparse, parse_qs
import os

# CHANGE THIS PATH TO YOUR POPPLER LOCATION
POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"

def extract_qr_data(pdf_path, dpi=400):
    try:

        if os.path.exists(POPPLER_PATH):
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=1,
                last_page=1,
                poppler_path=POPPLER_PATH
            )
        else:
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=1,
                last_page=1
            )

        if not images:
            return {"error": "Failed to convert PDF to image"}

        img = images[0]

        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        decoded_objects = decode(gray)

        if not decoded_objects:
            _, thresh = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            decoded_objects = decode(thresh)

        if not decoded_objects:
            enlarged = cv2.resize(
                gray,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC
            )
            decoded_objects = decode(enlarged)

        if not decoded_objects:
            decoded_objects = decode(img_cv)

        if not decoded_objects:
            return {"error": "No QR code detected in PDF"}

        raw_data = decoded_objects[0].data.decode("utf-8").strip()

        print("DEBUG - Raw QR:", raw_data)

        # DigiLocker JSON
        if raw_data.startswith("[") and raw_data.endswith("]"):
            try:
                parsed = json.loads(raw_data)

                return {
                    "success": True,
                    "issuer": "digilocker.gov.in",
                    "qr_url": raw_data,
                    "raw_payload": parsed
                }

            except Exception:
                pass

        parsed_url = urlparse(raw_data)
        params = parse_qs(parsed_url.query)

        cert_id = params.get("cert_id", params.get("c", [None]))[0]
        cert_hash = params.get("hash", params.get("h", [None]))[0]

        if cert_id and cert_hash:
            return {
                "success": True,
                "issuer": parsed_url.netloc,
                "qr_url": raw_data,
                "cert_id": cert_id,
                "expected_hash": cert_hash
            }

        if "::" in raw_data or raw_data.startswith("IN."):
            return {
                "success": True,
                "issuer": "digilocker.gov.in",
                "qr_url": raw_data
            }

        if raw_data.startswith("http"):

            domain = urlparse(raw_data).netloc

            return {
                "success": True,
                "issuer": domain,
                "verification_url": raw_data,
                "qr_url": raw_data
            }

        return {
            "error": f"QR found but unknown format.\nRaw Data: {raw_data}"
        }

    except Exception as e:
        return {
            "error": str(e)
        }