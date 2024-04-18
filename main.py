from PIL import Image
#from Crypto.Cipher import AES

# Encryption key
encryption_key = b"MrKrabsTotalsBaby"
pixel_count = 0

def main():
    img = Image.open("krab.jpg")
    pix = img.load()
    
    # Encrypt image
    encrypt_image(img, pix)

    # Save encrypted image
    img.save("encrypted_krab.jpg")
    print("Image encrypted and saved.") 
    
    # Decrypt image
    img = Image.open("encrypted_krab.jpg")
    pix = img.load()
    decrypt_image(img, pix)
    
    # Save decrypted image
    img.save("decrypted_krab.jpg")
    print("Image decrypted and saved.")

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

    # Convert binary string to bytes 
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
    # Step 1: Invert the bits
    inverted_bytes = ""
    for character in diffusion_bytes:
        if character == '0':
            inverted_bytes += '1'
        else:
            inverted_bytes += '0'
    
    # Step 2: Swap adjacent bits
    # Convert the inverted binary string to a list of characters
    binary_list = list(inverted_bytes)
    
    # Iterate through the list, swapping adjacent characters
    for i in range(0, len(binary_list) - 1, 2):
        binary_list[i], binary_list[i+1] = binary_list[i+1], binary_list[i]
    
    # Join the list back into a string
    swapped_binary_string = ''.join(binary_list)

    # Step 3: Shift bytes
    # Convert the swapped binary string to bytes
    num_bytes = (len(swapped_binary_string) + 7) // 8
    byte_data = int(swapped_binary_string, 2).to_bytes(num_bytes, byteorder='big')
    
    # Convert bytes back to integer
    int_data = int.from_bytes(byte_data, byteorder='big')
    int_data = int_data % 65536
    # Mask and shift the integer
    int_data = (int_data & 0x1fffff)
    
    # Convert the shifted integer back to bytes
    shifted_byte_data = int_data.to_bytes(2, byteorder='big')
    # Convert bytes to binary string
    binary_data = ''.join(format(byte, '08b') for byte in shifted_byte_data)

    # Padding if necessary
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

def xor_decrypt(binary_string: str, key: bytes):
    #Step 1: Convert binary string to bytes like what was done in the diffuse_decryption function

    #Step 2: xor bytes using this and key: xor_bytes = bytes(a ^ b for a, b in zip(byte_data, key))
    #Test Comment delete

    #Step 3: return binary string

    #Change var as necessary
    decrypted_string = ""
    return decrypted_string

def diffuse_decrypt(diffusion_bytes: str) -> str:

    #Step 1: Take the binary string diffusion_bytes and convert to bytes
    #I would suggest to put this into var 

    #Step 2: Take bytes and convert to int using the int.from_bytes() function
    #Again put it in a var

    #Step 3: Use this to shift back into place (<Int var here>, byteorder='big') << 24) & 0xffffff
    #Note: I don't know if this will get the exact values back.
    #I don't know if the bytes will change in the background since we are storing the image separably
    #If problems arise try to copy the bytes after they are shifted on line 80 into a list
    #And use them here

    #Step 4: Convert back to bytes using this: shifted_byte_data = int_data.to_bytes(2, byteorder='big')

    #Step 5: Convert back to binary string using this: binary_data = ''.join(format(byte, '08b') for byte in shifted_byte_data)

    #Step 6: Find a way to swap back the binary values from the loop on line 67
    #Example of the swapping loop: 1001 --> 0110
    #Example of the reverse loop: 0110 --> 1001

    #Step 7: Invert the binary numbers in the binary string
    # Example: 0011 --> 1100

    #Step 8: Return the binary string
    #Place holder variable. Change if need be or delete if need be
    binary_data = ""

    return binary_data
    
def decrypt_pixel(rgb_tuple):
    binary_string = rgb_to_binary(rgb_tuple)
    decrypted_diffused = diffuse_decrypt(binary_string)
    decrypted_xor = xor_decrypt(decrypted_diffused, encryption_key)
    decrypted_r = int(decrypted_xor[:8], 2)
    decrypted_g = int(decrypted_xor[8:16], 2)
    decrypted_b = int(decrypted_xor[16:], 2)
    return (decrypted_r, decrypted_g, decrypted_b)

def encrypt_image(img, pix):
    # Iterate over each pixel
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            #Encrypt pixel RGB values
            encrypted_rgb = encrypt_pixel(pix[x,y])
            #update pixel with encrypted values
            pix[x, y] = encrypted_rgb
            
def decrypt_image(img, pix):
    # Iterate over each pixel
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            # Decrypt pixel RGB values
            decrypted_rgb = decrypt_pixel(pix[x,y])
            #update pixel with encrypted values
            pix[x, y] = decrypted_rgb

if __name__ == "__main__":
    main()