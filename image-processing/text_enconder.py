import numpy as np

def char_into_bgr(c: np.uint8, bgr: np.array) -> np.array:
    assert bgr.dtype == np.uint8
    assert bgr.shape == (3,)

    b_bits = (c & 0b00000111)
    g_bits = (c & 0b00011000) >> 3
    r_bits = (c & 0b11100000) >> 5

    bgr[0] = (bgr[0] & 0b11111000) | b_bits
    bgr[1] = (bgr[1] & 0b11100111) | g_bits
    bgr[2] = (bgr[2] & 0b00011111) | r_bits

    return bgr

def bgr_into_char(bgr: np.array) -> np.uint8:
    assert bgr.dtype == np.uint8
    assert bgr.shape == (3,)

    c = np.uint8(0)
    c = (bgr[0] & 0b00000111 ) | c
    c = (bgr[1] & 0b00011000 ) | c
    c = (bgr[2] & 0b11100000 ) | c

    return c

def text_into_image(text: str, image: np.array) -> None:
    assert image.dtype == np.uint8

    # Create text header, which consists of 8 characters:
    # "TEXT" + 4 bytes representing the text length as an unsigned integer.
    len32 = np.uint32(len(text))
    len8_0 = np.uint8(len32 & 0b00000011)
    len8_1 = np.uint8((len32 & 0b00001100) >> 2)
    len8_2 = np.uint8((len32 & 0b00110000) >> 4)
    len8_3 = np.uint8((len32 & 0b11000000) >> 6)
    header = "TEXT" + chr(len8_3) + chr(len8_2) + chr(len8_1) + chr(len8_0)

    new_text = header + text
    new_len32 = np.uint32(len(new_text))
    assert new_len32 == len32 + 8
    #tarray = np.frombuffer(new_text.encode(), dtype=np.uint8, count=new_len32)

    for c in range(new_len32):
        i,j = divmod(c, image.shape[1])
        #image[i,j] = char_into_bgr(np.uint8(ord(new_text[c])), image[i,j])
        char_into_bgr(np.uint8(ord(new_text[c])), image[i,j])

def read_text_from_image(image: np.array) -> str:
    assert image.dtype == np.uint8

    # Read header
    chars = []
    for bgr in image[0,:8]:
        chars.append(bgr_into_char(bgr))
    header_text = '' + chr(chars[0]) + chr(chars[1]) + chr(chars[2]) + chr(chars[3])
    text_length = np.uint32(0)
    text_length = np.uint32(chars[4]) << 6 | text_length
    text_length = np.uint32(chars[5]) << 4 | text_length
    text_length = np.uint32(chars[6]) << 2 | text_length
    text_length = np.uint32(chars[7])      | text_length

    print(header_text)
    print(text_length)

