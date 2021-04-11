from morse import morse_text_processing
from itertools import groupby
from pydub import AudioSegment
import numpy as np

min_frequency = 200
window_duration = 2 / min_frequency
time_unit_range = (0.03, 0.3)
time_unit_default = 0.1

# returns mean squared amplitude averaged over non-overlapping windows
def signal_to_msa_chunks(signal, rate):
    samples_per_window = int(rate * window_duration)
    signal_squared = np.mean(signal * signal, axis=0)
    num_windows = int(np.ceil(np.size(signal_squared) / samples_per_window))
    padded_signal_length = num_windows * samples_per_window
    padded = np.pad(signal_squared, (0, padded_signal_length - np.size(signal_squared)))
    return padded.reshape(-1, samples_per_window).mean(axis=1)


def load_signal(filename):
    seg = AudioSegment.from_file(filename)
    channels = seg.split_to_mono()
    samples = [s.get_array_of_samples() for s in channels]
    arr = np.array(samples).astype(np.float32)
    arr /= np.iinfo(samples[0].typecode).max
    return arr, seg.frame_rate


def find_threshold(msa_chunks):
    return np.mean(msa_chunks)


def msa_to_on_off(msa_chunks, threshold):
    on = [
        (v, len(list(g))) for v, g in groupby(msa_chunks, lambda val: val > threshold)
    ]
    return [
        (v, l * window_duration)
        for v, l in on
        if l * window_duration >= time_unit_range[0]
    ]


def find_time_unit(on_off):
    min_duration = min(duration for v, duration in on_off)
    median_duration = np.median([duration for v, duration in on_off])
    result = (min_duration + median_duration) / 2
    if result >= time_unit_range[0] and result <= time_unit_range[1]:
        return result
    return time_unit_default


def gap_element(duration, time_unit):
    gap_durations = [
        (time_unit, ""),
        (3 * time_unit, " "),
        (7 * time_unit, "   "),
    ]
    _, gap_type = min((abs(duration - d), t) for d, t in gap_durations)
    return gap_type


def on_element(duration, time_unit):
    on_durations = [(time_unit, "."), (3 * time_unit, "-")]
    _, on_type = min((abs(duration - d), t) for d, t in on_durations)
    return on_type


def morse_element(value, duration, time_unit):
    if value:
        return on_element(duration, time_unit)
    else:
        return gap_element(duration, time_unit)


def on_off_to_morse_text(on_off, time_unit):
    return "".join(
        morse_element(v, duration, time_unit) for v, duration in on_off
    ).strip()


def process_signal(signal, rate):
    msa_chunks = signal_to_msa_chunks(signal, rate)
    threshold = find_threshold(msa_chunks)
    on_off = msa_to_on_off(msa_chunks, threshold)
    time_unit = find_time_unit(on_off)
    morse_text = on_off_to_morse_text(on_off, time_unit)
    text = morse_text_processing.decode(morse_text)
    return {
        "msa_chunks": msa_chunks,
        "on_off": on_off,
        "threshold": threshold,
        "time_unit": time_unit,
        "morse_text": morse_text,
        "plain_text": text,
    }


def process_soundfile(filename):
    signal, rate = load_signal(filename)
    return process_signal(signal, rate)
