import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_NEAREST)
    return result

def aligment_by_projection(img: np.array) -> float:

    def cost_function(profile) -> float:
        cost = 0.0
        for i in range(len(horizontal_sum) - 1):
            diff = profile[i+1]-profile[i]
            cost += diff * diff
        return cost

    assert len(img.shape) == 2  # img is grayscale
    img = img / 255.0

    max_cost = 0.0
    result_angle = 0.0
    for angle in np.linspace(-90.0, 90.0, 400):
        rot_img = rotate_image(img, angle)
        horizontal_sum = rot_img.sum(axis=1)
        cost = cost_function(horizontal_sum)
        if max_cost < cost:
            max_cost = cost
            result_angle = angle

    return result_angle


def main():
    img_path_str, out_img_path_str = parse_arguments()

    # Read image
    img = cv2.imread(img_path_str)
    if img.dtype != np.uint8:
        img = np.array(img, dtype=np.uint8)

    print(f"Input image: {img.shape[0]}x{img.shape[1]} pixels.")
    print(f"    {img_path_str}")
    print(f"Output image: {out_img_path_str}")

    # Make image grayscale.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold to make image binary.
    # In images of text files this should provide a good result most of the time.
    thr, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Invert the binary values: background now is black (0) and text is white (255).
    black_mask = (img == 0)
    white_mask = (img == 255)
    img[black_mask] = 255
    img[white_mask] = 0

    print(aligment_by_projection(img))



def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Text Aligner',
        description='Align image according to the angle detected.',
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
        out_img_path_str = str(Path(__file__).with_name(f"aligned_{img_path.stem}.png"))

    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    return img_path_str, out_img_path_str


if __name__ == "__main__":
    main()
