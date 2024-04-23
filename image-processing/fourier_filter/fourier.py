import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

def circle_mask(img: np.array, radius: int) -> np.array:
    assert len(img.shape) == 2
    cols, rows = img.shape
    mask = np.zeros(img.shape, dtype = np.uint8)
    for i in range(rows):
        for j in range(cols):
            shifted_i = i-rows/2
            shifted_j = j-cols/2
            mask[i,j] = 1 if shifted_i*shifted_i + shifted_j*shifted_j <= radius*radius else 0
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
    cv2.imwrite(out_img_path_str+"fft.png", np.abs(circle_mask(img_fft, 100)))

    # Write output image.
    img_restored = np.fft.ifft2(np.fft.fftshift(img_fft))
    cv2.imwrite(out_img_path_str, 255*abs(img_restored))




    def do_nothing(x):
        pass

    h, w = img_gray.shape
    img_left = np.zeros(img_gray.shape, np.uint8)
    img_left[:] = 255*img_gray

    img_middle = np.zeros(img_gray.shape, np.uint8)

    img_right = np.zeros(img_gray.shape, np.uint8)
    img_right[:] = 255*abs(img_restored)

    img = np.zeros((h, 3*w), np.uint8)
    img[:, 0:w] = img_left[:]
    img[:, 2*w:3*w] = img_right[:]

    # Create interactive window with sliders for parameter control.
    window = "Fourier Filter"
    inner = "Inner radius"
    outer = "Outer radius"
    cv2.namedWindow(window)
    cv2.createTrackbar(inner, window, 0, 100, do_nothing)
    cv2.createTrackbar(outer, window, 0, 100, do_nothing)

    # Switch FFT On/Off.
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, window, 0, 1, do_nothing)

    # Main loop.
    while(True):
        inner_r = cv2.getTrackbarPos(inner, window)
        outer_r = cv2.getTrackbarPos(outer, window)
        s = cv2.getTrackbarPos(switch, window)

        if s == 0:
            masked_fft = img_fft
        else:
            masked_fft = circle_mask(img_fft, inner_r)

        filtered = 255*abs(np.fft.ifft2(np.fft.fftshift(masked_fft)))
        img[:, w:2*w] = np.abs(masked_fft)
        img[:, 2*w:3*w] = np.abs(filtered)

        cv2.imshow(window, img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()



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
