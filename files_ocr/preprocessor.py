import cv2
import logging

from files_ocr.сonfiguration import Configuration


class Preprocessor:
    def __init__(self, config: Configuration):
        self.log = logging.getLogger(self.__class__.__name__)
        self.is_remove_horizontal_lines = config.remove_horizontal_lines
        self.is_grayscale = config.grayscale

    def remove_horizontal_lines(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (28, 1))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2))
        result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
        return result

    def prepare_img(self, image):
        if self.is_remove_horizontal_lines:
            image = self.remove_horizontal_lines(image)
        elif self.is_grayscale:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
