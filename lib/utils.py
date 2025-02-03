import logging
import qrcode
from PIL import Image
import requests
from io import BytesIO

logger = logging.getLogger(__name__)

class Utils:

    @staticmethod
    def _add_overlay(qr_code):
        logger.info("Starting to add overlay to QR code.")
        try:
            response = requests.get("https://discord.com/assets/dd05fd1ea37e7747.png")
            response.raise_for_status()
            logger.info("Overlay image fetched successfully.")
        except requests.RequestException as e:
            logger.error(f"Error fetching overlay image: {e}")
            return None

        try:
            overlay = Image.open(BytesIO(response.content)).convert("RGBA")
            overlay = overlay.resize((100, 100))
            logger.info("Overlay image processed successfully.")

            if qr_code.mode != "RGBA":
                qr_code = qr_code.convert("RGBA")

            bg_w, bg_h = qr_code.size
            offset = ((bg_w - overlay.size[0]) // 2, (bg_h - overlay.size[1]) // 2)
            qr_code.paste(overlay, offset, overlay)
            logger.info("Overlay added to QR code successfully.")
            return qr_code
        except Exception as e:
            logger.error(f"Error processing overlay image: {e}")
            return None

    @staticmethod
    def generate_qr_code(fingerprint):
        logger.info(f"Generating QR code for fingerprint: {fingerprint}")
        try:
            img = qrcode.make(f'https://discord.com/ra/{fingerprint}')
            logger.info("QR code generated successfully.")
            return img
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            return None

    @staticmethod
    def generate_qr_code_with_overlay(fingerprint):
        logger.info(f"Generating QR code with overlay for fingerprint: {fingerprint}")
        qr_code = Utils.generate_qr_code(fingerprint)
        if qr_code is None:
            logger.error("Failed to generate QR code.")
            return None
        return Utils._add_overlay(qr_code)