import pyaudio
import wave
import process

# set the audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# create the audio object
audio = pyaudio.PyAudio()

# open the microphone stream
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# print("Recording...")

# # create an empty list to store the audio data
# audio_data = []

# # record audio for a fixed number of seconds
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     audio_data.append(data)

# print("Finished recording.")

# # stop the stream and close the audio object
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # save the audio data to a WAV file
# wavefile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wavefile.setnchannels(CHANNELS)
# wavefile.setsampwidth(audio.get_sample_size(FORMAT))
# wavefile.setframerate(RATE)
# wavefile.writeframes(b''.join(audio_data))
# wavefile.close()

process.process()

