import logging
import pathlib
from configparser import ConfigParser


class Configuration:
    def __init__(self, cfg_path=None, args=None):
        self.log = logging.getLogger(self.__class__.__name__)

        # Initialize default values
        if args.input is not None:
            self.input_file_path = pathlib.Path(args.input)
        else:
            self.input_file_path = None
        if args.output is not None:
            self.output_file_path = pathlib.Path(args.output)
        else:
            self.output_file_path = None
        self.poppler_path = False
        self.grayscale = False
        self.tesseract_path = False
        self.remove_horizontal_lines = False
        self.oem = 3
        self.psm = 6

        # Parse config
        if cfg_path is not None:
            self.init_config_from_file(cfg_path)

    def init_config_from_file(self, cfg_path):
        cfg_path = pathlib.Path(cfg_path).resolve()
        self.log.info("Parsing configuration from .cfg file: '%s'", cfg_path)
        cfg: ConfigParser = ConfigParser()
        cfg.read(cfg_path)
        # general
        if self.input_file_path is None:
            self.input_file_path = pathlib.Path(cfg.get("general", "INPUT_FILE"))
        if self.output_file_path is None:
            self.output_file_path = pathlib.Path(cfg.get("general", "OUTPUT_FILE"))
        # input file
        self.poppler_path = pathlib.Path(cfg.get("inputfile", "POPPLER_PATH"))
        # preprocessor
        self.grayscale = cfg.get("preprocessor", "GRAYSCALE")
        self.remove_horizontal_lines = cfg.get("preprocessor", "REMOVE_HORIZONTAL_LINES")

        # OCR
        self.oem = cfg.get("ocr", "OEM")
        self.psm = cfg.get("ocr", "PSM")
        self.tesseract_path = pathlib.Path(cfg.get("ocr", "PATH_TESSERACT"))