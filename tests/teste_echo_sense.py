import pyaudio

p = pyaudio.PyAudio()

info = p.get_device_info_by_index(10)
print(info)

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024,
    input_device_index=10,
)

print("Stream abriu!")
stream.close()
p.terminate()