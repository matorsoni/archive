import numpy as np

def char_into_bgr(c: np.uint8, bgr: np.array) -> np.array:
    '''
    Encodes a uint8 character in a BGR (uint8) pixel by replacing the pixel's least
    significant bits per channel.
    3 bits in Blue, 2 bits in Green, 3 bits in Red.

    Example:
    Input 24-bit pixel BBBBBBBB|GGGGGGGG|RRRRRRRR
    Input 8-bit character 'X' == 88 == 01011000
    Output 24-bit pixel BBBBB000|GGGGGG11|RRRRR010
    '''
    assert bgr.dtype == np.uint8
    assert bgr.shape == (3,)

    b_bits = (c & 0b00000111)
    g_bits = (c & 0b00011000) >> 3
    r_bits = (c & 0b11100000) >> 5

    bgr[0] = (bgr[0] & 0b11111000) | b_bits
    bgr[1] = (bgr[1] & 0b11111100) | g_bits
    bgr[2] = (bgr[2] & 0b11111000) | r_bits

    return bgr

def bgr_into_char(bgr: np.array) -> np.uint8:
    '''
    Retrieves the character encoded by `char_into_bgr` in a BGR pixel.
    '''
    assert bgr.dtype == np.uint8
    assert bgr.shape == (3,)

    c = np.uint8(0)
    c = (bgr[0] & 0b00000111)      | c
    c = (bgr[1] & 0b00000011) << 3 | c
    c = (bgr[2] & 0b00000111) << 5 | c

    return c

def encode_text_into_image(text: str, image: np.array) -> None:
    assert image.dtype == np.uint8

    # Create text header, which consists of 8 characters:
    # "TEXT" + 4 bytes representing the text length as an unsigned integer.
    len32 = np.uint32(len(text))
    len8_0 = np.uint8( len32 & 0b11111111)
    len8_1 = np.uint8((len32 & (0b11111111 << 8)) >> 8)
    len8_2 = np.uint8((len32 & (0b11111111 << 16)) >> 16)
    len8_3 = np.uint8((len32 & (0b11111111 << 24)) >> 24)
    header = "TEXT" + chr(len8_3) + chr(len8_2) + chr(len8_1) + chr(len8_0)

    new_text = header + text
    new_len32 = np.uint32(len(new_text))
    assert new_len32 == len32 + 8

    for c in range(new_len32):
        i,j = divmod(c, image.shape[1])
        char_into_bgr(np.uint8(ord(new_text[c])), image[i,j])

def decode_text_from_image(image: np.array) -> str:
    assert image.dtype == np.uint8

    # Read header
    chars = []
    for bgr in image[0,:8]:
        chars.append(bgr_into_char(bgr))
    header_text = '' + chr(chars[0]) + chr(chars[1]) + chr(chars[2]) + chr(chars[3])
    text_length = np.uint32(0)
    text_length = (np.uint32(chars[4]) << 24) | text_length
    text_length = (np.uint32(chars[5]) << 16) | text_length
    text_length = (np.uint32(chars[6]) << 8)  | text_length
    text_length = np.uint32(chars[7])         | text_length

    if header_text != "TEXT":
        print(f"Decode error: invalid header \"{header_text}\", image has no encoded text.")
        return None

    chars = []
    text = ''
    for c in range(8, text_length + 8):
        i,j = divmod(c, image.shape[1])
        text += chr(bgr_into_char(image[i,j]))

    return text

def dump_img_bits(img: np.array, prefix: str = "img") -> None:
    '''
    For each channel in an image, write binary images to disk containing
    the n-th bits of that color. Mainly used for debugging.

    So, for 3 channels with 8 bits -> 24 binary images.
    '''
    import cv2

    assert img.dtype == np.uint8
    assert img.shape[2] == 3

    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]

    for i in range(8):
        # Take a grayscale 8bit channel and extract its n-th bit.
        # For n in (0,1,2,3,4,5,6,7) we have:
        # (c & 0b00000001) * 255
        # (c & 0b00000010) * 127
        # (c & 0b00000100) * 63, etc...
        # Note that most significant bits get attenuated: max values are (255,254,252,248,240,224,192,128).
        # But it's ok for now, since it's only used for debugging.
        cv2.imwrite( prefix + f"_b_bit{i}.png", (b & (1 << i)) * (255 >> i) )
        cv2.imwrite( prefix + f"_g_bit{i}.png", (g & (1 << i)) * (255 >> i) )
        cv2.imwrite( prefix + f"_r_bit{i}.png", (r & (1 << i)) * (255 >> i) )
