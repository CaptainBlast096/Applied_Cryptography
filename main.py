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

def xor_encrypt(binary_string: str, key: bytes): 

    #Convert binary string to bytes 
    num_bytes = (len(binary_string) + 7) // 8
    byte_data = int(binary_string, 2).to_bytes(num_bytes, byteorder='big')
    xor_bytes = bytes(a ^ b for a, b in zip(byte_data, key)) #This xor's the bytes
    binary_data = ''.join(format(byte, '08b') for byte in xor_bytes) #convert to string binary

   
    # Increment pixel count and print progress every 10000 pixels
    global pixel_count
    pixel_count += 1
    if (pixel_count % 10000) == 0:
        print("Number of pixels converted: " + str(pixel_count))


    return binary_data 

def diffuse_bytes(diffusion_bytes: str) -> str:

    inverted_bytes = ""

    for character in diffusion_bytes:
        if character == '0':
            inverted_bytes += '1'
        else:
            inverted_bytes += '0'
    

    # Convert the binary string to a list of characters
    binary_list = list(inverted_bytes)
    
    # Iterate through the list, swapping adjacent characters
    for i in range(0, len(binary_list) - 1, 2):
        binary_list[i], binary_list[i+1] = binary_list[i+1], binary_list[i]
    
    # Join the list back into a string
    swapped_binary_string = ''.join(binary_list)

    #shift bytes
    num_bytes = (len(swapped_binary_string) + 7) // 8
    byte_data = int(swapped_binary_string, 2).to_bytes(num_bytes, byteorder='big')
    int_data = int.from_bytes(byte_data, byteorder='big')
    int_data = (int_data & 0x1fffff) >> 24

    shifted_byte_data = int_data.to_bytes(2, byteorder='big')
    binary_data = ''.join(format(byte, '08b') for byte in shifted_byte_data)

    padding = 24 - len(binary_data)
    if padding <= 24:
        binary_data = ('0' * padding) + binary_data
    else:
        raise Exception("Binary Data is too large")

    return binary_data



    

def encrypt_pixel(rgb_tuple):
    binary_string = rgb_to_binary(rgb_tuple)
    encrypted_binary: str = xor_encrypt(binary_string, encryption_key)
    binary_diffused: str = diffuse_bytes(encrypted_binary)
    # Convert encrypted binary string back to RGB tuple
    encrypted_r = int(binary_diffused[:8], 2)
    encrypted_g = int(binary_diffused[8:16], 2)
    encrypted_b = int(binary_diffused[16:], 2)
    return (encrypted_r, encrypted_g, encrypted_b)


if __name__ == "__main__":
    main()