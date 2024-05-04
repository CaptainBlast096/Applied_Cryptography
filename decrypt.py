import hashlib
import numpy as np
from PIL import Image, ImageEnhance

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