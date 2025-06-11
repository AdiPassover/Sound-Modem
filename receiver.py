import numpy as np
import sounddevice as sd

from constants import (
    SAMPLE_RATE, FREQ_SS, FREQ_BIT0_1, FREQ_BIT0_2, FREQ_BIT1_1, FREQ_BIT1_2, FREQ_BIT2_0, FREQ_BIT2_1, FREQ_BIT2_2
)
THRESHOLD = 0.5
EPSILON = 50

def listen(duration):
    recording = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
    sd.wait()

    fft = np.fft.fft(recording[:, 0])
    freqs = np.fft.fftfreq(len(fft), 1 / SAMPLE_RATE)
    magnitude = np.abs(fft)
    return freqs, magnitude

def listen_for_freq(freq, duration, threshold=THRESHOLD, epsilon=EPSILON) -> bool:
    """Listen for a specific frequency tone for a given duration."""
    print(f"Listening for frequency {freq} Hz...")
    freqs, magnitude = listen(duration)
    idx = np.where(abs(freqs - freq) < epsilon)

    if np.max(magnitude[idx]) > threshold:
        print(f"Detected frequency {freq} Hz with magnitude {np.max(magnitude[idx]):.2f}")
        return True
    else:
        print(f"Frequency {freq} Hz not detected. (Magnitude: {np.max(magnitude[idx]):.2f})")
        return False

def is_freq(freqs, magnitude, target_freq, threshold=THRESHOLD, epsilon=EPSILON):
    """Check if a specific frequency is present in the recorded frequencies."""
    idx = np.where(abs(freqs - target_freq) < epsilon)
    if idx[0].size > 0 and np.max(magnitude[idx]) > threshold:
        return True
    return False

msg = ""
def receive():
    global msg
    msg = ""
    while True:
        if listen_for_freq(FREQ_SS, 0.2):
            break
    print("Start/Stop frequency detected. Listening for bits...")

    while True:
        is_finished = False
        curr_bits = [0, 0, 0]

        while True:
            freqs, magnitudes = listen(0.2)

            if is_freq(freqs, magnitudes, FREQ_BIT0_1):
                print("Bit0=1 frequency detected.")
                curr_bits[0] = 1
                continue
            elif is_freq(freqs, magnitudes, FREQ_BIT0_2):
                print("Bit0=2 frequency detected.")
                curr_bits[0] = 2
                continue
            elif is_freq(freqs, magnitudes, FREQ_BIT1_1):
                print("Bit1=1 frequency detected.")
                curr_bits[1] = 1
                continue
            elif is_freq(freqs, magnitudes, FREQ_BIT1_2):
                print("Bit1=2 frequency detected.")
                curr_bits[1] = 2
                continue
            elif is_freq(freqs, magnitudes, FREQ_BIT2_2):
                print("Bit2 frequency detected.")
                curr_bits[2] = 2
                break
            elif is_freq(freqs, magnitudes, FREQ_BIT2_1):
                print("Bit2 frequency detected.")
                curr_bits[2] = 1
                break
            elif is_freq(freqs, magnitudes, FREQ_BIT2_0):
                print("Bit2 OFF frequency detected.")
                break
            elif is_freq(freqs, magnitudes, FREQ_SS) and len(msg) > 0:
                print("Start/Stop frequency detected. Ending reception.")
                is_finished = True
                break

        if not is_finished:
            print(f"Received bits: {curr_bits}")
            curr_num = 0
            for i, bit in enumerate(curr_bits):
                curr_num += bit * (3**i)
            msg += str(curr_num)
        else:
            break
    print(f"Reception complete.\n Received bitstream: {msg}")





if __name__ == "__main__":
    print("Starting receiver...")
    try:
        receive()
    except KeyboardInterrupt:
        print(f"\nReceiver stopped by user.\n Message received: {msg}")
