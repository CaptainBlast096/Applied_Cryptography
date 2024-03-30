from PIL import Image
#from Crypto.Cipher import AES

# Encryption key
encryption_key = b"MrKrabsTotalsBaby"
pixel_count = 0

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
    encrypted_binary = xor_encrypt(binary_string, encryption_key)
    # Convert encrypted binary string back to RGB tuple
    encrypted_r = int(encrypted_binary[:8], 2)
    encrypted_g = int(encrypted_binary[8:16], 2)
    encrypted_b = int(encrypted_binary[16:], 2)
    return (encrypted_r, encrypted_g, encrypted_b)

def xor_encrypt(binary_string, key): 

    #print(binary_string)
    #Convert binary string to bytes 
    num_bytes = (len(binary_string) + 7) // 8
    byte_data = int(binary_string, 2).to_bytes(num_bytes, byteorder='big')
    my_bytes = bytes(a ^ b for a, b in zip(byte_data, key))
    binary_data = ''.join(format(byte, '08b') for byte in my_bytes) 

   
    global pixel_count
    pixel_count += 1
    if (pixel_count % 10000) == 0:
        print("Number of pixels converted: " + str(pixel_count))


    return binary_data 




if __name__ == "__main__":
    main()