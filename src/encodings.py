def is_letter_supported(letter: chr) -> bool:
    return ('a' <= letter <= 'z') or letter == ' '

def encode_letter(letter: chr) -> tuple[int, int, int]:
    if not is_letter_supported(letter):
        raise ValueError(f"Unsupported letter: {letter}")
    if letter == ' ':
        return 2,2,2
    num = ord(letter) - ord('a')
    bit0 = num % 3
    bit1 = (num // 3) % 3
    bit2 = (num // 9) % 3
    return bit0, bit1, bit2

def decode_letter(bits: tuple[int, int, int]) -> chr:
    if bits == (2,2,2):
        return ' '
    if not all(0 <= bit <= 2 for bit in bits):
        raise ValueError(f"Invalid bits: {bits}")
    num = bits[0] + bits[1] * 3 + bits[2] * 9
    return chr(num + ord('a'))