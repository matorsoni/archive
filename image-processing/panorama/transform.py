import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

# Access image clamping the edge values for out of bounds access.
def pixel(img, i, j):
    i = np.clip(i, 0, img.shape[0]-1)
    j = np.clip(j, 0, img.shape[1]-1)
    return img[i, j]

# Sampling modes.
def sample_nearest(img, i: float, j: float):
    return pixel(img, int(np.floor(i+0.5)), int(np.floor(j+0.5)))

def sample_bilinear(img, i: float, j: float):
    di = i - np.floor(i)
    dj = j - np.floor(j)
    i = int(i)
    j = int(j)
    sample  = (1.0-di) * (1.0-dj) * pixel(img, i, j)
    sample += di * (1.0-dj) * pixel(img, i+1, j)
    sample += (1.0-di) * dj * pixel(img, i, j+1)
    sample += di * dj * pixel(img, i+1, j+1)
    return sample

def sample_bicubic(img, i: float, j: float):
    def P(t):
        return max(0.0, t)

    def R(s):
        return 1.0/6.0 * (P(s+2)**3 - 4*P(s+1)**3 + 6*P(s)**3 - 4*P(s-1)**3)

    di = i - np.floor(i)
    dj = j - np.floor(j)
    i = int(i)
    j = int(j)
    sample = 0
    for m in [-1, 0, 1, 2]:
        for n in [-1, 0, 1, 2]:
            sample += pixel(img, i+m, j+n) * R(m-di) * R(dj-n)

    return sample

def sample_lagrange(img, i: float, j: float):
    pass
    di = i - np.floor(i)
    dj = j - np.floor(j)
    i = int(i)
    j = int(j)

    def L(n: int):
        val  = -1.0/6.0 * di*(di-1.0)*(di-2.0)*pixel(img, i-1, j+n-2)
        val += 1.0/2.0 * (di+1.0)*(di-1.0)*(di-2.0)*pixel(img, i, j+n-2)
        val += -1.0/2.0 * di*(di+1.0)*(di-2.0)*pixel(img, i+1, j+n-2)
        val += 1.0/6.0 * di*(di+1.0)*(di-1.0)*pixel(img, i+2, j+n-2)
        return val

    sample  = -1.0/6.0 * dj*(dj-1.0)*(dj-2.0)*L(1)
    sample +=  1.0/2.0 * (dj+1.0)*(dj-1.0)*(dj-2.0)*L(2)
    sample += -1.0/2.0 * dj*(dj+1.0)*(dj-2.0)*L(3)
    sample +=  1.0/6.0 * dj*(dj+1.0)*(dj-1.0)*L(4)
    return sample

def sampling_mode(mode: str):
    if mode == "nearest":
        return sample_nearest
    elif mode == "bilinear":
        return sample_bilinear
    elif mode == "bicubic":
        return sample_bicubic
    elif mode == "lagrange":
        return sample_lagrange
    assert False, "Invalid mode should not get here!!"

# Scale transform.
def apply_scale(img, scale, mode):
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
    sample = sampling_mode(mode)
    for I in range(H):
        for J in range(W):
            i = int(I / scale)
            j = int(J / scale)
            assert i < img.shape[0]
            assert j < img.shape[1]

            new_img[I, J] = sample(img, i, j)

    return new_img

# Rotation transform.
def apply_rotation(img, angle_deg, mode):
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
    sample = sampling_mode(mode)
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
                new_img[I, J] = sample(img, i, j)

    return new_img


def main():
    img_path_str, out_img_path_str, scale, angle, mode = parse_arguments()

    # Read image
    input_img = cv2.imread(img_path_str)
    if input_img.dtype != np.uint8:
        input_img = np.array(input_img, dtype=np.uint8)

    print(f"Input image:")
    print(f"    Path: {img_path_str}")
    print(f"    Dimensions: {input_img.shape[0]}x{input_img.shape[1]}")
    print(f"    Scale factor: {scale}")
    print(f"    Rotation angle: {angle}")
    print(f"    Interpolation mode: {mode}")

    out_img = input_img
    if scale != None:
        out_img = apply_scale(out_img, scale, mode)
    if angle != None:
        out_img = apply_rotation(out_img, angle, mode)

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

    parser.add_argument(
        '-m', '--mode',
        help="Interpolation mode, one of: nearest, bilinear, bicubic, lagrange",
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
    mode = args.mode

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
        print("Error: no transformation was provided.")
        sys.exit(1)

    if scale != None:
        scale = float(scale)
        if scale < 0.0:
            print("Error: scaling factor must be positive.")
            sys.exit(1)

    if angle != None:
        angle = float(angle)

    valid_mode = \
        mode == "nearest"  or  \
        mode == "bilinear" or  \
        mode == "bicubic"  or  \
        mode == "lagrange"

    if not valid_mode:
        print(f"Error: invalid interpolation mode \"{mode}\", see help (-h).")
        sys.exit(1)

    return img_path_str, out_img_path_str, scale, angle, mode


if __name__ == "__main__":
    main()
