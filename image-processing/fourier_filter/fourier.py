import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

def circle_mask(img: np.array, inner: int, outer: int, flip: bool) -> np.array:
    assert len(img.shape) == 2
    assert inner <= outer
    rows, cols = img.shape
    mask = np.ones(img.shape, dtype = bool)
    if flip:
        mask = ~mask

    # Input values range from 0 to 100, so divide by 200 to get radius
    inner_radius = int(inner/200.0 * min(rows, cols))
    outer_radius = int(outer/200.0 * min(rows, cols))
    # TODO: Rewrite with np.indices(img.shape)
    row_ind, col_ind = np.indices(img.shape, dtype=np.float32)
    row_ind -= rows/2.0
    col_ind -= cols/2.0
    inner_mask = row_ind*row_ind + col_ind*col_ind <= inner_radius*inner_radius
    outer_mask = row_ind*row_ind + col_ind*col_ind <= outer_radius*outer_radius
    mask[outer_mask] = ~mask[outer_mask]
    mask[inner_mask] = ~mask[inner_mask]

    return mask * img

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
    # If none is given, write to the same folder as this script
    if out_img_path_str is None:
        out_img_path_str = str(Path(__file__).with_name("filtered_" + img_path.name))

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

    # Convert to grayscale in [0, 1.0] float.
    img = img.astype(float) / 255.0
    img_gray = (img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3.0

    # Frequency domain image shifted to center.
    img_fft = np.fft.fftshift(np.fft.fft2(img_gray))

    # Interactive visualization
    # Allocate display image with size 3 times the input image
    h, w = img_gray.shape
    display_img = np.zeros((h, 3*w), np.uint8)
    display_img[:, 0:w] = 255*img_gray
    display_img[:, 2*w:3*w] = 0

    # Create interactive window with sliders for parameter control.
    window = "Fourier Filter"
    inner = "Inner radius"
    outer = "Outer radius"
    switch = "FFT filter On/Off"
    flip = "Flip filter On/Off"
    cv2.namedWindow(window)
    def do_nothing(x): pass   # Trackbar callback does not need to do anything
    cv2.createTrackbar(inner, window, 0, 100, do_nothing)
    cv2.setTrackbarPos(inner, window, 100)
    cv2.createTrackbar(outer, window, 0, 100, do_nothing)
    cv2.setTrackbarPos(outer, window, 100)
    cv2.createTrackbar(switch, window, 0, 1, do_nothing)
    cv2.createTrackbar(flip, window, 0, 1, do_nothing)

    # Main loop.
    while(True):
        # Read value set on the UI
        inner_r = cv2.getTrackbarPos(inner, window)
        outer_r = cv2.getTrackbarPos(outer, window)
        switch_on = cv2.getTrackbarPos(switch, window)
        flip_on = bool(cv2.getTrackbarPos(flip, window))

        if inner_r > outer_r:
            inner_r = outer_r
            cv2.setTrackbarPos(inner, window, outer_r)

        # Update frequency domain image with binary mask and also the final image
        masked_fft = img_fft if switch_on == 0 else circle_mask(img_fft, inner_r, outer_r, flip_on)
        filtered = 255*np.abs(np.fft.ifft2(np.fft.fftshift(masked_fft)))

        # Write images to the display and render
        display_img[:, w:2*w] = np.abs(masked_fft)
        display_img[:, 2*w:3*w] = filtered
        cv2.imshow(window, display_img)

        # Close window with the ESC key.
        # TODO: improve the close condition
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

    # Write frequency domain image to disk
    fft_img_path_str = str(Path(out_img_path_str).with_name("fft_filtered_" + img_path.name))
    cv2.imwrite(fft_img_path_str, np.abs(masked_fft))

    # Write output image to disk
    cv2.imwrite(out_img_path_str, filtered)



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
