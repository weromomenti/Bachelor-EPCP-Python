import librosa
import numpy as np
from scipy import signal

def compute_hps(cqt, N=3):
    returnCqt = np.copy(cqt)

    for n in range(1, N+1):
        downsampledCqt = cqt[:, ::2**n]
        downsampledCqt = np.repeat(a=downsampledCqt, repeats=2**n, axis=1)
        returnCqt *= downsampledCqt[:, :len(returnCqt[0])]

    return returnCqt