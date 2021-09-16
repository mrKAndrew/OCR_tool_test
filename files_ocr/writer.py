from pathlib import Path
import logging


class Writer:
    def __init__(self, output_file_path):
        self.log = logging.getLogger(self.__class__.__name__)
        self.encoding = 'utf-8'
        self.output_file_path = Path(output_file_path)
        if self.output_file_path.is_file():
            self.output_file_path.unlink()

    def write(self, text_result):
        try:
            with open(self.output_file_path, 'a', encoding=self.encoding) as f:
                f.write(text_result)
        except OSError:
            self.log.exception("Can't write file %s", self.output_file_path)
