import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import argparse

from constants import (
    SAMPLE_RATE, BIT_DURATION, DELIM_DURATION, FREQ_BIT, FREQ_DELIM, FREQ_SS, SS_DURATION
)
THRESHOLD = 0.5

def listen(duration):
    recording = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
    sd.wait()

    fft = np.fft.fft(recording[:, 0])
    freqs = np.fft.fftfreq(len(fft), 1 / SAMPLE_RATE)
    magnitude = np.abs(fft)
    return freqs, magnitude

def listen_for_freq(freq, duration, threshold=THRESHOLD, epsilon=50) -> bool:
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

def is_freq(freqs, magnitude, target_freq, threshold=THRESHOLD, epsilon=50):
    """Check if a specific frequency is present in the recorded frequencies."""
    idx = np.where(abs(freqs - target_freq) < epsilon)
    if idx[0].size > 0 and np.max(magnitude[idx]) > threshold:
        return True
    return False


# def listen_and_decode(bit_count):
#     print("Listening for bits...")
#     magnitudes_bit = []
#     magnitudes_delim = []
#     decoded_bits = []
#
#     for i in range(bit_count):
#         # Wait for delimiter tone
#         recording_delim = sd.rec(int(SAMPLE_RATE * DELIM_DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
#         sd.wait()
#         fft_delim = np.fft.fft(recording_delim[:, 0])
#         freqs = np.fft.fftfreq(len(fft_delim), 1 / SAMPLE_RATE)
#         mag_delim = np.abs(fft_delim)
#         idx_delim = np.where(abs(freqs - FREQ_DELIM) < 50)
#         delim_mag = np.max(mag_delim[idx_delim])
#         magnitudes_delim.append(delim_mag)
#
#         # Record bit slot
#         recording_bit = sd.rec(int(SAMPLE_RATE * BIT_DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
#         sd.wait()
#         fft_bit = np.fft.fft(recording_bit[:, 0])
#         freqs_bit = np.fft.fftfreq(len(fft_bit), 1 / SAMPLE_RATE)
#         mag_bit = np.abs(fft_bit)
#         idx_bit = np.where(abs(freqs_bit - FREQ_BIT) < 50)
#         bit_mag = np.max(mag_bit[idx_bit])
#         magnitudes_bit.append(bit_mag)
#
#         # Decision based on bit frequency magnitude
#         bit = "1" if bit_mag > THRESHOLD else "0"
#         decoded_bits.append(bit)
#         print(f"Bit {i+1}: {bit} (Bit Magnitude: {bit_mag:.2f}, Delim Magnitude: {delim_mag:.2f})")
#
#     # Plot magnitude values
#     x = np.arange(1, bit_count + 1)
#     plt.figure(figsize=(10, 5))
#     plt.plot(x, magnitudes_bit, label='Bit Magnitude (FREQ_BIT)', marker='o')
#     plt.plot(x, magnitudes_delim, label='Delimiter Magnitude (FREQ_DELIM)', marker='x')
#     plt.axhline(y=THRESHOLD, color='red', linestyle='--', label=f"Threshold = {THRESHOLD}")
#     plt.xlabel("Bit #")
#     plt.ylabel("Magnitude")
#     plt.title("Received Magnitudes Per Bit")
#     plt.legend()
#     plt.tight_layout()
#     plt.show()
#
#     print("\nDecoded bitstream:", ''.join(decoded_bits))


def receive():
    number = ""
    while True:
        if listen_for_freq(FREQ_SS, 0.2):
            break
    print("Start/Stop frequency detected. Listening for bits...")

    while True:
        is_finished = False
        curr_bit = "0"

        while True:
            freqs, magnitudes = listen(0.2)
            if is_freq(freqs, magnitudes, FREQ_DELIM):
                print("Delimiter frequency detected.")
                number += curr_bit
                break
            elif is_freq(freqs, magnitudes, FREQ_SS):
                print("Start/Stop frequency detected. Ending reception.")
                is_finished = True
                break
            elif is_freq(freqs, magnitudes, FREQ_BIT):
                print("Bit frequency detected. Continuing to listen for delimiter...")
                curr_bit = "1"
                continue

        if is_finished:
            break
    print(f"Reception complete.\n Received bitstream: {number}")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive bitstream via audio.")
    parser.add_argument("bits_to_receive", nargs="?", type=int, default=5, help="Number of bits to receive")
    args = parser.parse_args()

    if args.bits_to_receive <= 0:
        raise ValueError("bits_to_receive must be a positive integer.")

    print("Starting receiver...")
    receive()
