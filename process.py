import pyaudio
import wave
import numpy as np
import time
import librosa
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.ndimage
import soundfile as sf
from match_chords import match_chords
import hps

def process():

    y, sr = sf.read('CantinaBand60.wav', dtype='float32')
    y = y.T
    y = librosa.resample(y=y, orig_sr=sr, target_sr=22050)
    plots = 5

    #y = librosa.effects.preemphasis(y)
    #y = librosa.util.normalize(y)

    harmonic = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=1024)

    plt.figure(figsize=(20, 8))

    plt.subplot(plots, 1, 1)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Original Signal With Percussion')
    plt.tight_layout()

    downsampled = hps.compute_hps(harmonic)

    plt.subplot(plots, 1, 2)
    librosa.display.specshow(downsampled, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Downsampled (Work in Progress)')
    plt.tight_layout()

    y_harmonic, y_percussive = librosa.effects.hpss(y, margin=8)
    print(librosa.feature.tempo(y=y_percussive, sr=sr))

    harmonic = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=1024)

    plt.subplot(plots, 1, 3)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Chroma CQT')
    plt.tight_layout()

    harmonic = np.minimum(harmonic, librosa.decompose.nn_filter(harmonic, aggregate=np.average, metric='cosine'))

    plt.subplot(plots, 1, 4)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Non-local Filtered')
    plt.tight_layout()

    harmonic = scipy.ndimage.median_filter(harmonic, size=(1,9))
    #harmonic = hps.compute_hps(harmonic)

    plt.subplot(plots, 1, 5)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.title('Horizontal-median Filtered')
    #plt.xticks((0, 30))
    plt.colorbar()
    plt.tight_layout()

    plt.show()

    #match_chords(harmonic)


if __name__ == "__main__":
    process()