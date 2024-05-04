import encrypt
import decrypt
import hashlib
from PIL import Image, ImageEnhance
import numpy as np


# Splitting up the image into chunks
def split_image(image, chunk_size):
    width, height = image.size
    chunks = []
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            box = (x, y, x + chunk_size, y + chunk_size)
            chunks.append(image.crop(box))
    return chunks

def main():
    # Load image
    image = Image.open("Images\\krab.jpg")

    # Define chunk size and string key
    chunk_size = 100
    key = "mr krabs why would you do that"

    # Split image into chunks
    chunks = split_image(image, chunk_size)

    # Rearrange chunks based on the key with controlled randomness and distortion
    rearranged_chunks = encrypt.rearrange_chunks(chunks, key)

    new_image = Image.new("RGB", image.size)
    # Create a new image with rearranged and distorted chunks
    for i, chunk in enumerate(rearranged_chunks):
        x = (i * chunk_size) % image.width
        y = (i * chunk_size) // image.width * chunk_size
        new_image.paste(chunk, (x, y, x + chunk_size, y + chunk_size))

    # Display or save the new image
    new_image.show()
    new_image.save("Images\\image.jpg")

    # Load image
    encrypted_image = Image.open("Images\\image.jpg")

    # Split encrypted image into chunks
    encrypted_chunks = split_image(encrypted_image, 100)

    # Reverse chunk rearrangement using the same key
    reversed_rearranged_chunks = decrypt.reverse_rearrangement_chunks(encrypted_chunks, key)

    # Create a new image with rearranged and distorted chunks
    decrypted_image = Image.new("RGB", image.size)
    for i, chunk in enumerate(reversed_rearranged_chunks):
        x = (i * chunk_size) % image.width
        y = (i * chunk_size) // image.width * chunk_size
        decrypted_image.paste(chunk, (x, y, x + chunk_size, y + chunk_size))

    # Display or save the new image
    decrypted_image.show()
    decrypted_image.save("Images\\decrypted_image.jpg")


if __name__ == "__main__":
    main()
