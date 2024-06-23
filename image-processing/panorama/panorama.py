import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


def main():
    img_path_str, out_img_path_str = parse_arguments()

    # Read image
    input_img = cv2.imread(img_path_str)
    if input_img.dtype != np.uint8:
        input_img = np.array(input_img, dtype=np.uint8)

    print(f"Input image: {img_path_str}")
    print(f"Output image: {out_img_path_str}")

    # Convert image to grayscale.
    img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    # Write output image to disk
    #cv2.imwrite(out_img_path_str, out_img)

def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Panorama',
        description='Generate panorama from input images.',
    )

    parser.add_argument(
        '-i', '--input',
        help="Input image file (.jpeg, .png)",
        required=True,
    )

    parser.add_argument(
        '-o', '--output',
        help="Output image file (.png)",
        required=False,
    )

    return parser

def parse_arguments() -> tuple[str, str]:
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    out_img_path_str = args.output

    # Check input image path
    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    # Check output image path
    # If none is given, write to the same folder as this script
    if out_img_path_str is None:
        out_img_path_str = str(Path(__file__).with_name(f"panorama_{img_path.stem}.png"))

    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    return img_path_str, out_img_path_str


if __name__ == "__main__":
    main()
