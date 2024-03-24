import cv2


def main():
    img = cv2.imread("nhe.png")
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]

    # process channel red
    c = r

    # save a binary image with each bit of the input grayscale 8bit channel
    # (c & 0b00000001) * 255
    # (c & 0b00000010) * 127
    # (c & 0b00000100) * 63, etc...
    # most significant bits get attenuated: max value go like (255,254,252,248,240,224,192,128)
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

