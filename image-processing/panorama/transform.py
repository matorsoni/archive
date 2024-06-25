import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


# Scale transform
def apply_scale(img, scale):
    assert scale > 0.0

    # Computing width and height of scaled image.
    h = img.shape[0]
    w = img.shape[1]
    H = int(scale * h)
    W = int(scale * w)
    if len(img.shape) == 2:
        new_shape = (H, W)
    elif len(img.shape) == 3:
        new_shape = (H, W, img.shape[2])
    else:
        print(f"Unsupported image shape: {img.shape}")
        return None

    new_img = np.zeros(new_shape)
    for i in range(H):
        for j in range(W):
            i_orig = int(i / scale)
            j_orig = int(j / scale)
            assert i_orig < img.shape[0]
            assert j_orig < img.shape[1]

            new_img[i, j] = img[i_orig, j_orig]

    return new_img

def apply_rotation(img, angle_deg):
    angle = np.deg2rad(angle_deg)

    # Computing width and height of rotated image.
    h = img.shape[0]
    w = img.shape[1]
    c = np.abs(np.cos(angle))
    s = np.abs(np.sin(angle))
    H = int(h*c + w*s)
    W  = int(h*s + w*c)

    if len(img.shape) == 2:
        new_shape = (H, W)
    elif len(img.shape) == 3:
        new_shape = (H, W, img.shape[2])
    else:
        print(f"Unsupported image shape: {img.shape}")
        return None

    new_img = np.zeros(new_shape)
    for I in range(H):
        for J in range(W):
            # Compute pixel coordinates in [-0.5, 0.5]x[-0.5, 0.5] image space.
            X = J/W - 0.5
            Y = -I/H + 0.5

            # Apply rotation of -angle to retrieve x,y in original image space.
            # Then compute pixel indices in original image space.
            x = c * X + s * Y
            y = -s * X + c * Y
            i = int(0.5*h - y*H)
            j = int(0.5*w + x*W)

            if i >= 0 and i < h and j >= 0 and j < w:
                new_img[I,J] = img[i,j]

    return new_img


def main():
    img_path_str, out_img_path_str, scale, angle = parse_arguments()

    # Read image
    input_img = cv2.imread(img_path_str)
    if input_img.dtype != np.uint8:
        input_img = np.array(input_img, dtype=np.uint8)

    print(f"Input image:")
    print(f"    Path: {img_path_str}")
    print(f"    Dimensions: {input_img.shape[0]}x{input_img.shape[1]}")

    out_img = input_img
    if scale != None:
        out_img = apply_scale(out_img, scale)
    if angle != None:
        out_img = apply_rotation(out_img, angle)

    print(f"Output image:")
    print(f"    Path: {out_img_path_str}")
    print(f"    Dimensions: {out_img.shape[0]}x{out_img.shape[1]}")

    # Write output image to disk
    cv2.imwrite(out_img_path_str, out_img)

def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Geometric transformation',
        description='Apply rotation or scaling to input image.',
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
        '-s', '--scale',
        help="Scale value",
        required=False,
    )

    parser.add_argument(
        '-a', '--angle',
        help="Angle of rotation in degrees",
        required=False,
    )

    return parser

def parse_arguments() -> tuple[str, str]:
    parser = argparser()
    args = parser.parse_args()
    img_path_str = args.input
    out_img_path_str = args.output
    scale = args.scale
    angle = args.angle

    # Check input image path
    img_path = Path(img_path_str)
    if not img_path.exists() or not img_path.is_file():
        print(f"Invalid input image file name: {img_path_str}")
        sys.exit(1)

    # Check output image path
    # If none is given, write to the same folder as this script
    if out_img_path_str is None:
        out_img_path_str = str(Path(__file__).with_name(f"transformed_{img_path.stem}.png"))
    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    if scale == None and angle == None:
        print("Error: no transformation was provided")
        sys.exit(1)

    if scale != None:
        scale = float(scale)
        if scale < 0.0:
            print("Error: scaling factor must be positive")
            sys.exit(1)

    if angle != None:
        angle = float(angle)

    return img_path_str, out_img_path_str, scale, angle


if __name__ == "__main__":
    main()
