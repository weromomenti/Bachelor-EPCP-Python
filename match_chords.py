import numpy as np
import librosa 

def match_chords(harmonic: np.ndarray):

    n_slices = harmonic.shape[1]
    top_3_indices = np.zeros((n_slices, 6), dtype=int)
    
    for i in range(n_slices):
        slice_indices = np.argsort(harmonic[:, i])[-6:]
        top_3_indices[i] = slice_indices

    #max_notes = librosa.midi_to_note(max_vals)

    #largest_indices = sorted_indices[-3:]

    print()
