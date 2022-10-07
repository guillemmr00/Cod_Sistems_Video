import numpy as np


def run_length_encoder(seq):
    """
    This functions receives a string sequence and return the run-length encoded sequence.
    Args:
        seq (str): sequence that we want to encode with run-length

    Returns:
        x (str): encoded sequence

    """
    compressed = []
    count = 1
    char = seq[0]
    for i in range(1, len(seq)):
        if seq[i] == char:
            count = count + 1
        else:
            compressed.append([char, str(count)])
            char = seq[i]
            count = 1
    compressed.append([char, str(count)])
    x = np.concatenate(compressed)
    return ''.join(x)
