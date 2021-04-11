import simpleaudio as sa
import numpy as np
from morse import morse_text
import wave, struct

time_unit = 0.1
time_dot = time_unit
time_dash = 3 * time_unit
time_element_gap = time_unit
time_letter_gap = 3 * time_unit
time_word_gap = 7 * time_unit

morse_frequency = 700
sample_rate = 44100


def make_note(frequency, duration, volume=0.9):
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    buffer = np.sin(frequency * t * 2 * np.pi)
    audio = buffer * (volume / np.max(np.abs(buffer))) * (2 ** 15 - 1)
    return audio.astype(np.int16)


def make_gap(duration):
    return np.zeros(int(duration * sample_rate), dtype=np.int16)


def morse_single_element_buffer(morse_element):
    if morse_element == ".":
        return make_note(morse_frequency, time_dot)
    elif morse_element == "-":
        return make_note(morse_frequency, time_dash)
    elif morse_element == "e":
        return make_gap(time_element_gap)
    elif morse_element == "l":
        return make_gap(time_letter_gap)
    elif morse_element == "w":
        return make_gap(time_word_gap)


def morse_buffer(encoded_text):
    words = encoded_text.split("  ")
    words = [word.strip().split(" ") for word in words if len(word.strip()) > 0]
    elements = "w".join("l".join("e".join(letter) for letter in word) for word in words)
    return np.concatenate([morse_single_element_buffer(el) for el in elements])


def store_buffer(buffer, filename):
    wav_writer = wave.open(filename, "wb")
    wav_writer.setnchannels(1)
    wav_writer.setsampwidth(2)
    wav_writer.setframerate(sample_rate)
    wav_writer.writeframesraw(b"".join(buffer))


def morse_beep(text):
    encoded = morse_text.encode(text)
    buffer = morse_buffer(encoded)
    play = sa.play_buffer(buffer, 1, 2, sample_rate)
    play.wait_done()
