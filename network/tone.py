"""Produce nine seconds of raw G.711 PCMU audio for SIPp RTP streaming."""
from pathlib import Path
import math


def pcmu(sample):
    magnitude = min(abs(sample), 32635) + 132
    exponent = magnitude.bit_length() - 8
    mantissa = (magnitude >> (exponent + 3)) & 15
    sign = 128 if sample < 0 else 0
    return (~(sign | exponent << 4 | mantissa)) & 255


if __name__ == "__main__":
    samples = (int((900 + 6 * (index // 160)) * math.sin(2 * math.pi * 440 * index / 8000))
               for index in range(72000))
    Path("tone.pcmu").write_bytes(bytes(map(pcmu, samples)))
