import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

from utils import encode_text_into_image, dump_img_bits

def main():
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    text_path_str = args.text
    out_img_path_str = args.output

    # Check input image path
    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    # Check input text path
    if text_path_str is None:
        text_path_str = str(Path(__file__).parent / "default_text.txt")

    text_path = Path(text_path_str)

    if not text_path.exists() or not text_path.is_file():
        print("Invalid input text file name: {text_path_str}")
        sys.exit(1)

    # Check output image path
    if out_img_path_str is None:
        out_img_path_str = str(img_path.parent / f"encoded_{img_path.stem}.png")

    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    # Read inputs
    img = cv2.imread(img_path_str)
    img_size = img.shape[0] * img.shape[1]
    text = text_path.read_text()
    text_length = len(text)

    print(f"Input image: {img_size} ({img.shape[0]}x{img.shape[1]}) RGB pixels.")
    print(f"    {img_path_str}")
    print(f"Input text: {text_length} characters.")
    print(f"    {text_path_str}")

    if img_size < text_length + 8:
        print("Error: Text is too long to fit reasonably in the input image.")
        sys.exit(1)

    print(f"Output image: {out_img_path_str}")

    if img.dtype != np.uint8:
        img = np.array(img, dtype=np.uint8)

    # Uncomment to dump input image bits
    #dump_img_bits(img, prefix="in")

    encode_text_into_image(text, img)

    # Uncomment to dump output image bits
    #dump_img_bits(img, prefix="out")

    cv2.imwrite(out_img_path_str, img)

def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='encoder',
        description='Encode text into an image.',
    )

    parser.add_argument(
        '-i', '--input',
        help="Input image file (.jpeg or .png)",
        required=True,
    )

    parser.add_argument(
        '-t', '--text',
        help="Input text file (.txt)",
        required=False,
    )

    parser.add_argument(
        '-o', '--output',
        help="Output image file (.png)",
        required=False,
    )

    return parser


if __name__ == "__main__":
    main()
