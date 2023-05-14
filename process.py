from matplotlib.animation import FuncAnimation
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
from plot import plot

def process(y, sr):

    #y, sr = librosa.load('StarWars60.wav', offset=10, duration=10)

    #y = librosa.util.normalize(y)
    #y = librosa.effects.preemphasis(y)

    #harmonic1 = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=1024)
    #plot(harmonic, 'Original Signal With Percussion', plots)

    #downsampled = hps.compute_hps(harmonic1)
    #plot(downsampled, 'Original Signal with HPS', plots)
    #harmonic2 = vocalSeperation(y, sr)

    y_harmonic, y_percussive = librosa.effects.hpss(y)

    tempo = librosa.feature.tempo(y=y_percussive, sr=sr)

    # sf.write('harmonic.wav', y_harmonic, sr)
    # sf.write('percussive.wav', y_percussive, sr)
    # print(librosa.feature.tempo(y=y_percussive, sr=sr))


    harmonic2 = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=1024)
    harmonic2 = hps.compute_hps(harmonic2)

    #plot(harmonic, 'Chroma CQT', plots)

    # harmonic = np.minimum(harmonic, librosa.decompose.nn_filter(harmonic, aggregate=np.median, metric='cosine'))
    # plot(harmonic, 'Non-local Filtered', plots)

    # harmonic = scipy.ndimage.median_filter(harmonic, size=(1,9))
    # plot(harmonic, 'Horizontal-median Filtered', plots)

    return (harmonic2, tempo)