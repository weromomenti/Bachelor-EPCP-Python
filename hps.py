import librosa
import numpy as np


def compute_hps(cqt, N=3):
    returnCqt = np.ones_like(cqt)

    for n in range(N+1):
        downsampledCqt = cqt[::, ::2**n]
        downsampledCqt = np.pad(downsampledCqt, ((0, 0), (0, cqt.shape[1] - downsampledCqt.shape[1])))
        returnCqt *= downsampledCqt

    return returnCqt