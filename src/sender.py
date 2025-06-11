import numpy as np
import sounddevice as sd

from src.constants import (
    SAMPLE_RATE, SINGLE_DURATION, SS_DURATION,
    FREQ_SS, FREQ_BIT0_1, FREQ_BIT0_2, FREQ_BIT1_1, FREQ_BIT1_2, FREQ_BIT2_0, FREQ_BIT2_1, FREQ_BIT2_2
)
from src import encodings


def generate_tone(freq, duration=SINGLE_DURATION):
    """Generate a sine wave at a specific frequency and duration."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def quiet_tone(duration=SINGLE_DURATION):
    """Generate a silent tone for the specified duration."""
    return np.zeros(int(SAMPLE_RATE * duration))

def send_bitstream(bitstream: list[tuple[int, int, int]]):
    print("Sending preamble delimiter...")
    ss_tone = generate_tone(FREQ_SS, SS_DURATION)
    sd.play(ss_tone, SAMPLE_RATE)
    sd.wait()

    print("Sending bitstream...")
    for bits in bitstream:
        bit0, bit1, bit2 = bits
        print(f"Sending bits: {[bit0, bit1, bit2]} ({encodings.decode_letter(bits)})")

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

def send(message: str):
    if not all(encodings.is_letter_supported(letter) for letter in message):
        raise ValueError("Message can only contain lowercase letters and spaces.")

    encoded_msg = [encodings.encode_letter(letter) for letter in message]

    try:
        send_bitstream(encoded_msg)
    except KeyboardInterrupt:
        print("\nTransmission interrupted by user.")
