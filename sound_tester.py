import numpy as np
import sounddevice as sd

import constants

def generate_tone(freq, duration):
    """Generate a sine wave at a specific frequency and duration."""
    t = np.linspace(0, duration, int(constants.SAMPLE_RATE * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


def play_sound(freq, duration):
    """Play a sound at a specific frequency and duration."""
    tone = generate_tone(freq, duration)
    sd.play(tone, samplerate=constants.SAMPLE_RATE)
    sd.wait()


if __name__ == "__main__":
    print("Playing preamble...")
    play_sound(constants.FREQ_SS, constants.SS_DURATION)

    print("Playing bit tone (1)...")
    play_sound(constants.FREQ_BIT, constants.BIT_DURATION)

    print("Playing silence for bit 0...")
    play_sound(0, constants.BIT_DURATION)

    print("Playing delimiter tone...")
    play_sound(constants.FREQ_DELIM, constants.DELIM_DURATION)

    print("Playing start/stop tone...")
    play_sound(constants.FREQ_SS, constants.SS_DURATION)

    print("Sound test complete.")