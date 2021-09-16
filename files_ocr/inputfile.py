import os
import logging
import stat
import numpy as np
import cv2
from pdf2image import convert_from_path

from files_ocr.сonfiguration import Configuration


class InputFile:
    def __init__(self, file_path, config: Configuration):
        self.log = logging.getLogger(self.__class__.__name__)
        self._set_file_format(file_path)
        self._set_file_path(file_path)
        self.poppler_path = config.poppler_path

    def read(self) -> list:
        self.log.debug("Reading file '%s'", self.file_path)
        cv2_images = []
        try:
            if self.file_format == '.pdf':
                if not self.poppler_path or self.poppler_path is None:
                    raise ValueError('PopplerError')
                pages = convert_from_path(
                    self.file_path,
                    poppler_path=self.poppler_path)
                for page_number, page_data in enumerate(pages):
                    cv2_images.append(np.array(page_data))
                    self.log.debug("Read page # %s", page_number)
            elif self.file_format in ['.png', '.jpg']:
                cv2_images.append(cv2.imread(str(self.file_path)))
            return cv2_images
        except ValueError:
            self.log.exception("Poppler path is bad")
            raise

    def _set_file_format(self, file_path):
        self.file_format = os.path.splitext(file_path)[1].lower()
        if self.file_format in ['.png', '.jpg', '.pdf']:
            pass
        else:
            raise ValueError(f"File '{file_path}' bad format.\n Argument filename must be of type *.png, *.jpg, *.pdf")

    def _set_file_path(self, file_path):
        def can_open_file(filepath):
            if not os.path.isfile(filepath):
                return False
            return bool(os.stat(filepath).st_mode & stat.S_IRGRP)

        if can_open_file(file_path):
            self.file_path = file_path
        else:
            raise IOError(f"Can't open file '{file_path}'")
