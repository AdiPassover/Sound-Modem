import numpy as np
import sounddevice as sd
import argparse

from constants import (
    SAMPLE_RATE, SINGLE_DURATION, FREQ_BIT0, FREQ_BIT1, FREQ_SS, SS_DURATION, FREQ_BIT2, FREQ_BIT2_OFF
)

def generate_tone(freq, duration=SINGLE_DURATION):
    """Generate a sine wave at a specific frequency and duration."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def quiet_tone(duration=SINGLE_DURATION):
    """Generate a silent tone for the specified duration."""
    return np.zeros(int(SAMPLE_RATE * duration))

def send_bitstream(bitstream):
    print("Sending preamble delimiter...")
    ss_tone = generate_tone(FREQ_SS, SS_DURATION)
    sd.play(ss_tone, SAMPLE_RATE)
    sd.wait()

    print("Sending bitstream...")
    for num_str in bitstream:
        num = int(num_str)
        bit0, bit1, bit2 = bool(num & 1), bool(num & 2), bool(num & 4)

        if bit0:
            print("Sending bit0=1...")
            sd.play(generate_tone(FREQ_BIT0), SAMPLE_RATE)
        else:
            print("Sending bit0=0...")
            sd.play(quiet_tone(), SAMPLE_RATE)
        sd.wait()

        if bit1:
            print("Sending bit1=1...")
            sd.play(generate_tone(FREQ_BIT1), SAMPLE_RATE)
        else:
            print("Sending bit1=0...")
            sd.play(quiet_tone(), SAMPLE_RATE)
        sd.wait()

        if bit2:
            print("Sending bit2=1...")
            sd.play(generate_tone(FREQ_BIT2), SAMPLE_RATE)
        else:
            print("Sending bit2=0...")
            sd.play(generate_tone(FREQ_BIT2_OFF), SAMPLE_RATE)
        sd.wait()


    print("Sending postamble delimiter...")
    sd.play(ss_tone, SAMPLE_RATE)
    sd.wait()
    print("Transmission complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send bitstream via audio.")
    parser.add_argument("bitstream", nargs="?", default="10101", help="Bitstream to send (e.g., 10101)")
    args = parser.parse_args()

    if not all(bit in "01234567" for bit in args.bitstream):
        raise ValueError("Bitstream must only contain 0 or 1.")

    try:
        send_bitstream(args.bitstream)
    except KeyboardInterrupt:
        print("\nTransmission interrupted by user.")
