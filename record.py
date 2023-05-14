import time
import process
import sounddevice as sd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
import sys
from serial import Serial
import soundcard as sc

def record_system_sound(duration, sr):
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sr) as mic:
        data = mic.record(numframes=sr*duration)

    return data.flatten()

def update_plot():
    global duration

    audio_chunk = record_system_sound(duration, sr)
    (chroma, stuff) = process.process(audio_chunk, sr)

def index_to_chord(index):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',
             'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[index]

def plot_code():
    app = QtWidgets.QApplication(sys.argv)
    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle('Chroma CQT Real-Time Visualization')
    plot = win.addPlot(title="Chroma CQT")
    img = pg.ImageItem()
    plot.addItem(img)
    plot.setAspectLocked(True)
    #plot.invertY(True)  # Invert Y-axis to match the 'lower' origin

    # Set colormap
    cmap = pg.colormap.get('viridis')
    lut = cmap.getLookupTable(0.0, 1.0, 256)
    img.setLookupTable(lut)
    img.setLevels([0, 1])

    # Set axis labels
    plot.setLabel('left', 'Chroma')
    plot.setLabel('bottom', 'Time')

    # Update plot in real-time
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update_plot)
    timer.start(int(duration * 1000))

    # Start the Qt event loop
    sys.exit(app.exec_())

def sum_elements(arr):
    result = []
    # sum majors
    for i in range(len(arr)):
        sum_value = arr[i] + arr[(i + 4) % len(arr)] + arr[(i + 7) % len(arr)]
        result.append(sum_value)
    
    # sum minors
    for i in range(len(arr)):
        sum_value = arr[i] + arr[(i + 3) % len(arr)] + arr[(i + 7) % len(arr)]
        result.append(sum_value)

    return result

def main():
    global duration, sr

    COM_PORT = 'COM8'

    duration = 0.1  # Record duration in seconds for each chunk
    sr = 48000  # Sample rate

    #ser = Serial(COM_PORT, baudrate=9600)
    time.sleep(2)

    currentChord = ""
    prevChord = ""
    chords = []

    try:
        while True:
            frame = record_system_sound(duration, sr)
            (frame, bpm) = process.process(frame, sr)
            bpm = int(bpm)
            row_sums = np.sum(frame, axis=1)

            summed = sum_elements(row_sums)
            maxIndex = np.argmax(summed)

            if (summed[maxIndex] < 5):
                continue
            
            currentChord = index_to_chord(maxIndex)
            chords.append(currentChord)

            if (len(set(chords)) != 1):
                chords = []
                chords.append(currentChord)
            
            if len(chords) == 3 and len(set(chords)) == 1:
                if (prevChord != currentChord):
                    #ser.write(currentChord.encode())
                    chords = []
                    chords.append(currentChord)
                prevChord = currentChord

            print(currentChord)

    except KeyboardInterrupt:
        #ser.close()
        print("Stopped")
    
if __name__ == '__main__':
    main()


