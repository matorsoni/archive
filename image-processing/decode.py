import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

from text_enconder import *

def main():
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    text_path_str = args.output

    # Check received arguments

    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    if text_path_str is None:
        text_path_str = str(img_path.with_name("decoded_text.txt"))

    out_text_path = Path(text_path_str)

    # Read inputs
    img = cv2.imread(img_path_str)
    print(f"Input image: {img.shape[0]}x{img.shape[1]} pixels.")
    print(f"    {img_path_str}")

    assert img.dtype == np.uint8

    text = read_text_from_image(img)
    if text == None:
        sys.exit(1)

    print(f"Decoded text length: {len(text)} characters")
    print(f"    {str(out_text_path)}")

    out_text_path.write_text(text)

def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='decoder',
        description='Decode text from an image.',
    )

    parser.add_argument(
        '-i', '--input',
        help="Input image file (.png)",
        required=True,
    )

    parser.add_argument(
        '-o', '--output',
        help="Output text file (.txt)",
        required=False,
    )

    return parser


if __name__ == "__main__":
    main()
