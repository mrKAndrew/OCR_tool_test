import pytesseract
import logging

from files_ocr.сonfiguration import Configuration


class Recognizer:
    def __init__(self, config: Configuration):
        self.log = logging.getLogger(self.__class__.__name__)
        self.config_tesseract = f'--oem {config.oem} --psm {config.psm}'
        if config.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = str(config.tesseract_path)
        else:
            self.log.exception("Pytesseract path not found")
            raise ValueError('PytesseractError')

    def recognize(self, img):
        return pytesseract.image_to_string(img, config=self.config_tesseract)
