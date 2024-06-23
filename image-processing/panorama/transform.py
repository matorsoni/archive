import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


# Scale transform
def scale(img, scale):
    assert scale > 0.0

    new_height = int(scale * img.shape[0])
    new_width  = int(scale * img.shape[1])
    if len(img.shape) == 2:
        new_shape = (new_height, new_width)
    elif len(img.shape) == 3:
        new_shape = (new_height, new_width, img.shape[2])
    else:
        print(f"Unsupported image shape: {img.shape}")
        return None

    new_img = np.zeros(new_shape)
    for i in range(new_img.shape[0]):
        for j in range(new_img.shape[1]):
            i_orig = int(i / scale)
            j_orig = int(j / scale)
            #assert i_orig < img.shape[0]
            #assert j_orig < img.shape[1]

            new_img[i, j] = img[i_orig, j_orig]

    return new_img

def rotation(img, angle_deg):
    angle = np.deg2rad(angle_deg)

    # computing BB for new image
    a = img.shape[0]
    b = img.shape[1]
    # TODO: CORRIGIR O SINAL DO ANGULO, PRA OBTER UM GIRO CORRETO EM TODO O 360
    c = np.abs(np.cos(angle))
    s = np.abs(np.sin(angle))
    #c = np.cos(angle)
    #s = np.sin(angle)

    new_height = int(a*c + b*s)
    new_width  = int(a*s + b*c)
    if len(img.shape) == 2:
        new_shape = (new_height, new_width)
    elif len(img.shape) == 3:
        new_shape = (new_height, new_width, img.shape[2])
    else:
        print(f"Unsupported image shape: {img.shape}")
        return None
    new_img = np.zeros(new_shape)

    R = new_img.shape[0]
    C = new_img.shape[1]
    for I in range(R):
        for J in range(C):
            X = J/C - 0.5
            Y = -I/R + 0.5
            # Apply rotation of -angle to retrieve x,y in original image space
            x = c * X + s * Y
            y = -s * X + c * Y
            #i = int((0.5 - y)*R)  <-- centro errado
            #j = int((0.5 + x)*C)  <-- escala certa
            #i = int((0.5 - y)*a)  <-- centro correto
            #j = int((0.5 + x)*b)  <-- escala errada
            i = int(0.5*a - y*R) # YES
            j = int(0.5*b + x*C) # YES
            if i >= 0 and i < a and j >= 0 and j < b:
                new_img[I,J] = img[i,j]

    return new_img


def main():
    img_path_str, out_img_path_str = parse_arguments()

    # Read image
    input_img = cv2.imread(img_path_str)
    if input_img.dtype != np.uint8:
        input_img = np.array(input_img, dtype=np.uint8)

    print(f"Input image:")
    print(f"    Path: {img_path_str}")
    print(f"    Dimensions: {input_img.shape[0]}x{input_img.shape[1]}")

    out_img = scale(input_img, 2.2)
    out_img = rotation(out_img, 90.0)

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
        out_img_path_str = str(Path(__file__).with_name(f"transformed_{img_path.stem}.png"))

    if Path(out_img_path_str).suffix != ".png":
        print("Error: output image must be .png")
        sys.exit(1)

    return img_path_str, out_img_path_str


if __name__ == "__main__":
    main()
