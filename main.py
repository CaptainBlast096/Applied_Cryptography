import hashlib
from PIL import Image, ImageEnhance
import numpy as np


# random, unique, add noise

def split_image(image, chunk_size):
    width, height = image.size
    chunks = []
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            box = (x, y, x + chunk_size, y + chunk_size)
            chunks.append(image.crop(box))
    return chunks


def apply_distortion(chunk):
    # Apply distortion to the chunk (e.g., adding noise, rotating, etc.)
    # For demonstration, let's add Gaussian noise and adjust brightness
    chunk = chunk.convert('RGB')  # Provides image with 3 RGB channels (Red, Green, Blue)
    enhancer = ImageEnhance.Brightness(chunk)
    chunk = enhancer.enhance(0.5)  # Reduce brightness by 50%
    chunk_array = np.array(chunk)
    # chunk_array represents a chunk as a 2D numpy array of three color channels
    noise = np.random.normal(scale=30, size=chunk_array.shape).astype(np.uint8)
    # noise is using the gaussian noise distribution
    chunk_array += noise  # Save the noise and inverse the sign to -=
    return Image.fromarray(chunk_array)


def reverse_distortion(chunk):
    chunk = chunk.convert('RGB')
    enhancer = ImageEnhance.Brightness(chunk)
    chunk = enhancer.enhance(-0.5)
    chunk_array = np.array(chunk)

    noise = np.random.normal(scale=30, size=chunk_array.shape).astype(np.uint8)
    chunk_array -= noise  # Save the noise and inverse the sign to -=
    return Image.fromarray(chunk_array)


def rearrange_chunks(chunks, key):
    key_hash = hashlib.sha256(key.encode()).digest()
    key_index = int.from_bytes(key_hash, byteorder='big')

    # Seed the random number generator with the hash of the key
    rng = np.random.default_rng(key_index)  # Save the random value

    # Generate a random permutation of indices
    permuted_indices = rng.permutation(len(chunks))
    # Take the reverse of the array starting from the end backwards

    # Rearrange chunks based on the permuted indices
    rearranged_chunks = [None] * len(chunks)
    for i, index in enumerate(permuted_indices):
        chunk = apply_distortion(chunks[index])
        rearranged_chunks[i] = chunk
    return rearranged_chunks


def reverse_rearrangement_chunks(chunks, key):
    key_hash = hashlib.sha256(key.encode()).digest()
    key_index = int.from_bytes(key_hash, byteorder='big')

    # Seed the random number generator with the hash of the key
    rng = np.random.default_rng(key_index)

    original_indices = rng.permutation(len(chunks))

    inverse_permuted_indices = original_indices

    # Rearrange chunks based on the permuted indices
    rearranged_chunks = [None] * len(chunks)
    for i, index in enumerate(inverse_permuted_indices):
        rearranged_chunks[index] = chunks[i]
    return rearranged_chunks


def main():
    # Load image
    image = Image.open("krab.jpg")

    # Define chunk size and string key
    chunk_size = 100
    key = "mr krabs why would you do that"

    # Split image into chunks
    chunks = split_image(image, chunk_size)

    # Rearrange chunks based on the key with controlled randomness and distortion
    rearranged_chunks = rearrange_chunks(chunks, key)

    new_image = Image.new("RGB", image.size)
    # Create a new image with rearranged and distorted chunks
    for i, chunk in enumerate(rearranged_chunks):
        x = (i * chunk_size) % image.width
        y = (i * chunk_size) // image.width * chunk_size
        new_image.paste(chunk, (x, y, x + chunk_size, y + chunk_size))

    # Display or save the new image
    new_image.show()
    new_image.save("image.jpg")

    # Load image
    encrypted_image = Image.open("image.jpg")

    # Split encrypted image into chunks
    encrypted_chunks = split_image(encrypted_image, 100)

    # Reverse chunk rearrangement using the same key
    reversed_rearranged_chunks = reverse_rearrangement_chunks(encrypted_chunks, key)

    # Create a new image with rearranged and distorted chunks
    decrypted_image = Image.new("RGB", image.size)
    for i, chunk in enumerate(reversed_rearranged_chunks):
        x = (i * chunk_size) % image.width
        y = (i * chunk_size) // image.width * chunk_size
        decrypted_image.paste(chunk, (x, y, x + chunk_size, y + chunk_size))

    # Display or save the new image
    decrypted_image.show()
    decrypted_image.save("decrypted_image.jpg")


if __name__ == "__main__":
    main()
