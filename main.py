import argparse
import logging

from files_ocr.ocr import OCR
from files_ocr.сonfiguration import Configuration


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=False, default=None, help='input file *.pdf, *.png *.jpg')
    parser.add_argument('-o', '--output', required=False, default=None, help='output file')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    return parser.parse_args()


def setup_logging(verbose):
    if verbose == 0:
        logging.basicConfig(format="%(levelname)s: %(message)s")
    elif verbose == 1:
        level = logging.INFO
        logging.basicConfig(format="%(levelname)s: %(message)s", level=level)
    else:
        level = logging.DEBUG
        logging.basicConfig(format="%(levelname)s: %(message)s", level=level)


def main():
    args = arguments()
    setup_logging(args.verbose)
    config = Configuration(cfg_path=r'config.cfg', args=args)
    my_ocr = OCR(config)
    my_ocr.run()


if __name__ == '__main__':
    main()
