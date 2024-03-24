import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

from text_enconder import *

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

    return parser

def dump_img_bits(img: np.array, prefix: str = "img") -> None:
    '''
    For each channel in an image, write binary images to disk containing
    the n-th bits of that color. Mainly used for debugging.

    So, for 3 channels with 8 bits -> 24 binary images.
    '''

    def _extract_bit_n(c: np.array, n: int) -> np.array:
        '''
        Take a grayscale 8bit channel and extract its n-th bit.
        For n = (0,1,2,3,4,5,6,7) we have:
        (c & 0b00000001) * 255
        (c & 0b00000010) * 127
        (c & 0b00000100) * 63, etc...

        Note that most significant bits get attenuated: max values are (255,254,252,248,240,224,192,128).
        But it's ok for now, since it's only used for debugging.
        '''
        assert n >= 0 and n < 8
        return (c & (1 << n)) * (255 >> n)

    assert img.dtype == np.uint8
    assert img.shape[2] == 3

    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]

    for i in range(8):
        cv2.imwrite( prefix + f"_b_bit{i}.png", (b & (1 << i)) * (255 >> i) )
        cv2.imwrite( prefix + f"_g_bit{i}.png", (g & (1 << i)) * (255 >> i) )
        cv2.imwrite( prefix + f"_r_bit{i}.png", (r & (1 << i)) * (255 >> i) )


def main():
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    text_path_str = args.text

    # Check received arguments
    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    out_img_path_str = str(img_path.parent / f"encoded_{img_path.name}")

    if text_path_str is None:
        text_path_str = str(Path(__file__).parent / "default_text.txt")

    text_path = Path(text_path_str)

    if not text_path.exists() or not text_path.is_file():
        print("Invalid input text file name: {text_path_str}")
        sys.exit(1)

    # Read inputs
    img = cv2.imread(img_path_str)
    text = text_path.read_text()
    print(f"Input image: {img.shape[0]}x{img.shape[1]} pixels.")
    print(f"Input text: {len(text)} characters.")

    if img.dtype != np.uint8:
        img = np.array(img, dtype=np.uint8)

    dump_img_bits(img, prefix="in")

    text_into_image(text, img)

    dump_img_bits(img, prefix="out")

    t = read_text_from_image(img)

    cv2.imwrite("nho.png", img)

if __name__ == "__main__":
    main()

