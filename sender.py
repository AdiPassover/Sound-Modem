import numpy as np
import sounddevice as sd
import argparse

from constants import SAMPLE_RATE, BIT_DURATION, DELIM_DURATION, FREQ_BIT, FREQ_DELIM, FREQ_SS, SS_DURATION

def generate_tone(freq, duration):
    """Generate a sine wave at a specific frequency and duration."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def send_bitstream(bitstream):
    print("Sending preamble delimiter...")
    ss_tone = generate_tone(FREQ_SS, SS_DURATION)
    sd.play(ss_tone, SAMPLE_RATE)
    sd.wait()

    print("Sending bitstream...")
    for bit in bitstream:
        if bit == "1":
            sd.play(generate_tone(FREQ_BIT, BIT_DURATION), SAMPLE_RATE)
        else:
            sd.play(np.zeros(int(SAMPLE_RATE * BIT_DURATION)), SAMPLE_RATE)
        sd.wait()

        sd.play(generate_tone(FREQ_DELIM, DELIM_DURATION), SAMPLE_RATE)
        sd.wait()

    print("Sending postamble delimiter...")
    sd.play(ss_tone, SAMPLE_RATE)
    sd.wait()
    print("Transmission complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send bitstream via audio.")
    parser.add_argument("bitstream", nargs="?", default="10101", help="Bitstream to send (e.g., 10101)")
    args = parser.parse_args()

    if not all(bit in "01" for bit in args.bitstream):
        raise ValueError("Bitstream must only contain 0 or 1.")

    send_bitstream(args.bitstream)
