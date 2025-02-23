import time
import numpy as np
import sounddevice as sd
import librosa
import serial
from tensorflow.keras.models import load_model

# 1) Load AI model
model = load_model("keras_model.h5")

# 2) Connect to Arduino 
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow Serial to initialize

# 3) Configuration
DURATION = 2.0         # seconds of audio
SAMPLE_RATE = 16000    # Ensure this matches your training in Teachable Machine
N_MFCC = 43            
N_FFT = 512            # FFT window size
HOP_LENGTH = 69        # Step size (aligned for ~232 frames)

labels = ["Background", "LOUD", "QUIET"]  # Ensure this matches metadata.json

def record_audio(duration=DURATION, sample_rate=SAMPLE_RATE):
    """Capture 'duration' seconds of audio from PC mic and normalize."""
    print("\n Recording audio...")
    samples = int(duration * sample_rate)
    
    # Record as int16
    recording = sd.rec(samples, samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()

    # Convert int16 → float32 (-1 to 1)
    audio_wave = recording.astype(np.float32) / 32768.0
    audio_wave = np.squeeze(audio_wave)

    # Normalize audio (avoid divide by zero)
    max_val = np.max(np.abs(audio_wave))
    if max_val > 0:
        audio_wave = audio_wave / max_val

    # Debug: Print audio sample values
    print(" Audio sample values (first 10):", audio_wave[:10])
    
    return audio_wave

while True:
    # A) Record audio
    audio_wave = record_audio()

    # B) Compute MFCC
    mfcc = librosa.feature.mfcc(
        y=audio_wave,
        sr=SAMPLE_RATE,
        n_mfcc=N_MFCC,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        fmax=8000
    )

    print(" Before trimming/padding:", mfcc.shape)
    time_frames = mfcc.shape[1]

    # Ensure correct shape (Trim or Pad to 232 frames)
    if time_frames > 232:
        mfcc = mfcc[:, :232]
    elif time_frames < 232:
        mfcc = np.pad(mfcc, ((0,0), (0, 232 - time_frames)), mode='constant')

    print(" After trim/pad:", mfcc.shape)  # Should be (43, 232)

    # C) Reshape for the model
    mfcc = np.expand_dims(mfcc, axis=0)  # (1, 43, time_frames)
    mfcc = np.expand_dims(mfcc, axis=-1) # (1, 43, time_frames, 1)

    # D) Predict
    prediction = model.predict(mfcc)

    # Extract confidence scores
    background_conf = prediction[0][0]
    loud_conf = prediction[0][1]
    quiet_conf = prediction[0][2]

    # Debug: Print confidence scores
    print(f" Background: {background_conf:.3f}, LOUD: {loud_conf:.3f}, QUIET: {quiet_conf:.3f}")

    # E) Adjusted Classification Logic: Treat Background as QUIET
    if loud_conf > 0.6:  # LOUD detection
        final_label = "LOUD"
    else:  # Treat both Background and QUIET as "QUIET"
        final_label = "QUIET"

    print(f" Detected: {final_label}")

    # F) Send result to Arduino
    if final_label == "LOUD":
        arduino.write("LOUD\n".encode())
    else:  # QUIET and Background both send "QUIET"
        arduino.write("QUIET\n".encode())

    # G) Wait before next recording
    time.sleep(2)

