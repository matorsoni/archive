import argparse
from pathlib import Path
import sys

import cv2

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

    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]

    # process channel red
    c = r

    # Save a binary image with each bit of the input grayscale 8bit channel
    # (c & 0b00000001) * 255
    # (c & 0b00000010) * 127
    # (c & 0b00000100) * 63, etc...
    #
    # Note that most significant bits get attenuated: max values are (255,254,252,248,240,224,192,128)
    # but it's ok for now
    for i in range(8):
        cv2.imwrite( f"bit{i}_in.png", (c & (1 << i)) * (255 >> i) )

    #c = c & 0
    c = c & 0b11111000 # clear last 3 bits
    c = c | 0b00000111 # add new last 3 bits

    for i in range(8):
        cv2.imwrite( f"bit{i}_out.png", (c & (1 << i)) * (255 >> i) )

    out = img
    out[:,:,0] = b
    out[:,:,1] = g
    out[:,:,2] = c

    cv2.imwrite("nho.png", img)

if __name__ == "__main__":
    main()

