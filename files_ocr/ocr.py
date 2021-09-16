import logging

from files_ocr.inputfile import InputFile
from files_ocr.сonfiguration import Configuration
from files_ocr.preprocessor import Preprocessor
from files_ocr.recognizer import Recognizer
from files_ocr.writer import Writer


class OCR:
    def __init__(self, config: Configuration):
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.preprocessor = Preprocessor(config)
        self.recognizer = Recognizer(config)
        self.writer = Writer(config.output_file_path)

    def _process_file(self, input_file: InputFile):
        self.log.info("Processing file '%s'", input_file.file_path)
        result_text = ''
        try:
            list_imgs = input_file.read()
            len_of_imgs = len(list_imgs)
            for i_img, img in enumerate(list_imgs):
                # Preprocessing
                self.log.debug("Preprocessing img %s of %s", i_img + 1, len_of_imgs)
                img = self.preprocessor.prepare_img(img)
                # Recognition
                self.log.debug("Recognition img %s of %s", i_img + 1, len_of_imgs)
                result_text += self.recognizer.recognize(img)
                # Postprocessing (here we can add some action with recognized text)
            # Writing results
            self.writer.write(result_text)
        except Exception:
            self.log.exception("Error during processing file '%s'", input_file.file_path)

    def run(self):
        self.log.info("Starting OCR")
        input_file = InputFile(file_path=self.config.input_file_path, config=self.config)
        self._process_file(input_file)
