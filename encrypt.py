import hashlib
import numpy as np
from PIL import Image, ImageEnhance

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