import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

from text_enconder import *

def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='decoder',
        description='Decode text from an image.',
    )

    parser.add_argument(
        '-i', '--input',
        help="Input image file (.jpeg or .png)",
        required=True,
    )

    return parser

def main():
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input

    # Check received arguments
    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    out_text_path = img_path.with_name("decoded_text.txt")

    # Read inputs
    img = cv2.imread(img_path_str)
    print(f"Input image: {img.shape[0]}x{img.shape[1]} pixels.")

    assert img.dtype == np.uint8

    text = read_text_from_image(img)
    if text == None:
        sys.exit(1)

    print(f"Decoded text length: {len(text)} characters")

    out_text_path.write_text(text)

if __name__ == "__main__":
    main()
