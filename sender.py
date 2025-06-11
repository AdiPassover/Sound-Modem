import numpy as np
import sounddevice as sd
import argparse

from constants import (
    SAMPLE_RATE, SINGLE_DURATION, SS_DURATION,
    FREQ_SS, FREQ_BIT0_1, FREQ_BIT0_2, FREQ_BIT1_1, FREQ_BIT1_2, FREQ_BIT2_0, FREQ_BIT2_1, FREQ_BIT2_2
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

        bit0 = num % 3
        bit1 = (num // 3) % 3
        bit2 = (num // 9) % 3
        print(f"Sending bits: {[bit0, bit1, bit2]}")

        if bit0 == 1:
            sd.play(generate_tone(FREQ_BIT0_1), SAMPLE_RATE)
        elif bit0 == 2:
            sd.play(generate_tone(FREQ_BIT0_2), SAMPLE_RATE)
        else:
            sd.play(quiet_tone(), SAMPLE_RATE)
        sd.wait()

        if bit1 == 1:
            sd.play(generate_tone(FREQ_BIT1_1), SAMPLE_RATE)
        elif bit1 == 2:
            sd.play(generate_tone(FREQ_BIT1_2), SAMPLE_RATE)
        else:
            sd.play(quiet_tone(), SAMPLE_RATE)
        sd.wait()

        if bit2 == 1:
            sd.play(generate_tone(FREQ_BIT2_1), SAMPLE_RATE)
        elif bit2 == 2:
            sd.play(generate_tone(FREQ_BIT2_2), SAMPLE_RATE)
        else:
            sd.play(generate_tone(FREQ_BIT2_0), SAMPLE_RATE)
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
