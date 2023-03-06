import pyaudio
import wave
import numpy as np
import time
import librosa
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.ndimage
import soundfile as sf

def process():

    #filename = librosa.ex('ImperialMarch60.wav')

    y, sr = sf.read('ImperialMarch60.wav', dtype='float32')
    y = y.T
    y = librosa.resample(y=y, orig_sr=sr, target_sr=11025)

    #y = librosa.effects.preemphasis(y)
    #y = librosa.util.normalize(y)

    y_harmonic, y_percussive = librosa.effects.hpss(y, margin=8)

    wavfile.write('harmonic.wav', rate=sr, data=y_harmonic)
    wavfile.write('percussive.wav', rate=sr, data=y_percussive)

    harmonic = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=1024)

    plt.figure(figsize=(20, 8))
    
    plt.subplot(3, 1, 1)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Chroma CQT')
    plt.tight_layout()

    harmonic = np.minimum(harmonic, librosa.decompose.nn_filter(harmonic, aggregate=np.median, metric='cosine'))

    plt.subplot(3, 1, 2)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title('Non-local Filtered')
    plt.tight_layout()

    harmonic = scipy.ndimage.median_filter(harmonic, size=(1,9))

    plt.subplot(3, 1, 3)
    librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.title('Horizontal-median Filtered')
    #plt.xticks((0, 30))
    plt.colorbar()
    plt.tight_layout()

    #plt.figure(figsize=(10, 4))

    # for i in range (1,4):

    #     plt.subplot(4, 1, i)
    #     librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    #     plt.colorbar()

    #     downsampled = librosa.core.resample(harmonic, orig_sr=sr, target_sr=(sr // (2**i)))
    #     upsampled = librosa.core.resample(downsampled, orig_sr=(sr // (2**i)), target_sr=sr)
    #     upsampled = upsampled[0:len(harmonic), :len(harmonic[0])]
    #     harmonic *= upsampled

    # The drawing part
    # plt.figure(figsize=(10, 6))
    # plt.subplot(2,1,1)
    # librosa.display.specshow(harmonic, y_axis='chroma', x_axis='time')
    # plt.title('Harmonic Spectogram')
    # plt.colorbar()
    # plt.tight_layout()

    # plt.subplot(2,1,2)
    # librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
    # plt.title('Percussive Spectogram')
    # plt.colorbar()
    # plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    process()