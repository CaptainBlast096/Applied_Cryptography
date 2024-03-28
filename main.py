from PIL import Image

# Encryption key
encryption_key = b"MrKrabsTotalsBaby"

def main():
    img = Image.open("krab.jpg")
    pix = img.load()

    # Iterate over each pixel
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            #Encrypt pixel RGB values
            encrypted_rgb = encrypt_pixel(pix[x,y])
            #update pixel with encrypted values
            pix[x, y] = encrypted_rgb

    # Save encrypted image
    img.save("encrypted_krab.jpg")
    print("Image encrypted and saved.")           

def rgb_to_binary(rgb_tuple):
    r, g, b = rgb_tuple
    # Convert each component to binary and pad to 8 bits
    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')
    # Concatenate the binary strings
    binary_string = r_bin + g_bin + b_bin
    return binary_string

def encrypt_pixel(rgb_tuple):
    binary_string = rgb_to_binary(rgb_tuple)

if __name__ == "__main__":
    main()