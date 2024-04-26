import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

def circle_mask(img: np.array, radius: int) -> np.array:
    assert len(img.shape) == 2
    cols, rows = img.shape
    mask = np.zeros(img.shape, dtype = np.uint8)
    mask_radius = int(radius/200.0 * min(rows, cols))
    # TODO: Rewrite with np.indices(img.shape)
    for i in range(rows):
        for j in range(cols):
            shifted_i = i-rows/2
            shifted_j = j-cols/2
            mask[i,j] = 1 if shifted_i*shifted_i + shifted_j*shifted_j <= mask_radius*mask_radius else 0
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
    cv2.namedWindow(window)
    def do_nothing(x): pass   # Trackbar callback does not need to do anything
    cv2.createTrackbar(inner, window, 0, 100, do_nothing)
    cv2.createTrackbar(outer, window, 0, 100, do_nothing)

    # Switch FFT On/Off.
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, window, 0, 1, do_nothing)

    # Main loop.
    while(True):
        # Read value set on the UI
        inner_r = cv2.getTrackbarPos(inner, window)
        outer_r = cv2.getTrackbarPos(outer, window)
        s = cv2.getTrackbarPos(switch, window)

        # Update frequency domain image with binary mask and also the final image
        masked_fft = img_fft if s == 0 else circle_mask(img_fft, inner_r)
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
