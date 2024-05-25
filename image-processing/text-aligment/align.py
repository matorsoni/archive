import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


def rotate_image(image: np.array, angle: float):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
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

def alignment_by_hough(img: np.array):
    assert len(img.shape) == 2  # img is grayscale
    edge_img = cv2.Canny(img, 50, 200, None, 3)
    rho_accuracy = 1
    theta_accuracy = np.pi / 180
    vote_threshold = 30
    lines_acc = cv2.HoughLinesWithAccumulator(edge_img, rho_accuracy, theta_accuracy, vote_threshold, None, 0, 0)

    theta_acc = 0.0
    votes_acc = 0.0
    for i in range(min(3, len(lines_acc))):
        rho, theta, votes = lines_acc[i][0]
        theta_acc += theta * votes
        votes_acc += votes

    angle = theta_acc / votes_acc

    return np.rad2deg(angle) - 90.0

def main():
    img_path_str, out_img_path_str, mode = parse_arguments()

    # Read image
    input_img = cv2.imread(img_path_str)
    if input_img.dtype != np.uint8:
        input_img = np.array(input_img, dtype=np.uint8)

    print(f"Input image: {img_path_str}")
    print(f"Output image: {out_img_path_str}")
    print(f"Mode: {mode}")

    # Convert image to grayscale.
    img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    # Apply threshold to make image binary.
    # In images of text files this should provide a good result most of the time.
    thr, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    # Invert the binary values: background now is black (0) and text is white (255).
    black_mask = (img == 0)
    white_mask = (img == 255)
    img[black_mask] = 255
    img[white_mask] = 0

    if mode == "PROJ":
        angle = aligment_by_projection(img)
        print(f"Alignment angle: {angle:02f} degrees")
    else:
        assert mode == "HOUGH"
        angle = alignment_by_hough(img)
        print(f"Alignment angle: {angle:02f} degrees")

    # Write output image to disk
    cv2.imwrite(out_img_path_str, rotate_image(input_img, angle))

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

    parser.add_argument(
        '-m', '--mode',
        help="Align mode: either PROJ or HOUGH",
        required=True,
    )

    return parser

def parse_arguments() -> tuple[str, str]:
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    out_img_path_str = args.output
    mode = args.mode

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

    if mode != "PROJ" and mode != "HOUGH":
        print("Error: mode must be either PROJ or HOUGH")
        sys.exit(1)

    return img_path_str, out_img_path_str, mode


if __name__ == "__main__":
    main()
