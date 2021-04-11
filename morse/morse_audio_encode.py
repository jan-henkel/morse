import simpleaudio as sa
import numpy as np
from morse import morse_text_processing
import wave, struct

time_unit = 0.1
time_dot = time_unit
time_dash = 3 * time_unit
time_element_gap = time_unit
time_letter_gap = 3 * time_unit
time_word_gap = 7 * time_unit

morse_frequency = 700
sample_rate = 44100


def tone_audio_buffer(frequency, duration, volume=0.9):
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    buffer = np.sin(frequency * t * 2 * np.pi)
    audio = buffer * (volume / np.max(np.abs(buffer))) * (2 ** 15 - 1)
    return audio.astype(np.int16)


def gap_audio_buffer(duration):
    return np.zeros(int(duration * sample_rate), dtype=np.int16)


def morse_element_to_audio_buffer(morse_element):
    if morse_element == ".":
        return tone_audio_buffer(morse_frequency, time_dot)
    elif morse_element == "-":
        return tone_audio_buffer(morse_frequency, time_dash)
    elif morse_element == "e":
        return gap_audio_buffer(time_element_gap)
    elif morse_element == "l":
        return gap_audio_buffer(time_letter_gap)
    elif morse_element == "w":
        return gap_audio_buffer(time_word_gap)


def morse_text_to_audio_buffer(morse_text):
    words = morse_text.split("  ")
    words = [word.strip().split(" ") for word in words if len(word.strip()) > 0]
    elements = "w".join("l".join("e".join(letter) for letter in word) for word in words)
    return np.concatenate([morse_element_to_audio_buffer(el) for el in elements])


def text_to_audio_buffer(text):
    morse_text = morse_text_processing.encode(text)
    return morse_text_to_audio_buffer(morse_text)


def save_audio_buffer(audio_buffer, filename):
    wav_writer = wave.open(filename, "wb")
    wav_writer.setnchannels(1)
    wav_writer.setsampwidth(2)
    wav_writer.setframerate(sample_rate)
    wav_writer.writeframesraw(b"".join(audio_buffer))


def play_audio_buffer(audio_buffer):
    play = sa.play_buffer(audio_buffer, 1, 2, sample_rate)
    play.wait_done()