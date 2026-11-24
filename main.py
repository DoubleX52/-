from pygame import *   
import sounddevice as sd
import scipy.io.wavfile as wav

# === Налаштування ===
fs = 44100     
chunk = 1024   
width, height = 800, 400
recording = None
is_recording = None
voice_file = "voice_record.wav"
minus_track = "24.11\\MinusDuHast.mp3"

init()
screen = display.set_mode((width, height))
display.set_caption("Live Audio (Mic)")
clock = time.Clock()

# Початкові дані — масив нулів (ще немає звуку)
data = [0.0] * chunk

# === Функція, яку викликає sounddevice, коли приходить нова порція звуку ===
def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)

    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]

# === Запуск потоку з мікрофона ===
stream = sd.InputStream(
    callback=audio_callback,  
    channels=1,               
    samplerate=fs,             
    blocksize=chunk,           
    dtype='float32'            
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Готуємо список точок для малювання хвилі
    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)          
        y = int(height / 2 + sample)        
        points.append((x, y))               

    # Малюємо лінію по точках, якщо їх більше однієї
    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    display.update()
    clock.tick(60)

stream.stop()
quit()