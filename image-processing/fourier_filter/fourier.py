import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

def main():
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
    if out_img_path_str is None:
        out_img_path_str = str(img_path.with_name("filtered_" + img_path.name))

    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    # Read image
    img = cv2.imread(img_path_str)
    if img.dtype != np.uint8:
        img = np.array(img, dtype=np.uint8)

    print(f"Input image: {img.shape[0]}x{img.shape[1]} pixels.")
    print(f"    {img_path_str}")
    print(f"Output image: {out_img_path_str}")

    ## Interactive Fourier Filter

    ## Write output image
    cv2.imwrite(out_img_path_str, img)


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Fourier Filter',
        description='Filter grayscale image in the frequency domain with Fourier Transform.',
    )

    parser.add_argument(
        '-i', '--input',
        help="Input image file (.png)",
        required=True,
    )

    parser.add_argument(
        '-o', '--output',
        help="Output image file (.png)",
        required=False,
    )

    return parser


if __name__ == "__main__":
    main()
