from PIL import Image

def main():
    img = Image.open("krab.jpg")
    pix = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            print(pix[x,y])

def rgb_to_binary(rgb_tuple):
    r, g, b = rgb_tuple
    # Convert each component to binary and pad to 8 bits
    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')
    # Concatenate the binary strings
    binary_string = r_bin + g_bin + b_bin
    return binary_string

if __name__ == "__main__":
    main()