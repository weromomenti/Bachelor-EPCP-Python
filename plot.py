import matplotlib.pyplot as plt
import librosa

index = 1

def plot(y, name, plots, sr=22050):

    global index

    plt.subplot(plots, 1, index)
    index +=1
    librosa.display.specshow(y, y_axis='chroma', x_axis='time', sr=sr, hop_length=1024)
    plt.colorbar()
    plt.title(name)
    plt.tight_layout()