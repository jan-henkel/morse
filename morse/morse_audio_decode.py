from morse.morse_audio import sample_rate
from morse.morse_text import decode
from itertools import groupby
from pydub import AudioSegment
import numpy as np

min_frequency = 200
window_duration = 2 / min_frequency
time_unit_range = (0.03, 0.3)
time_unit_default = 0.1


def windowed_mean_squared_amplitude(signal, signal_sample_rate):
    samples_per_window = int(signal_sample_rate * window_duration)
    num_windows = (np.size(signal) + samples_per_window - 1) // samples_per_window
    padded_signal_length = num_windows * samples_per_window
    signal_padded = np.pad(signal, (0, padded_signal_length - np.size(signal)))
    signal_squared = signal_padded * signal_padded
    return signal_squared.reshape(-1, samples_per_window).mean(axis=1)


def load_file(filename):
    seg = AudioSegment.from_file(filename)
    channels = seg.split_to_mono()
    samples = [s.get_array_of_samples() for s in channels]
    arr = np.array(samples).T.astype(np.float32)
    arr /= np.iinfo(samples[0].typecode).max
    return arr.T, seg.frame_rate


def find_threshold(mean_squared_amp):
    return np.mean(mean_squared_amp)


def convert_to_on_off(mean_squard_amp, threshold):
    on = [
        (v, len(list(g)))
        for v, g in groupby(mean_squard_amp, lambda val: val > threshold)
    ]
    return [
        (v, l * window_duration)
        for v, l in on
        if l * window_duration >= time_unit_range[0]
    ]


def find_time_unit(on_off_buffer):
    m = min(duration for v, duration in on_off_buffer)
    if m >= time_unit_range[0] and m <= time_unit_range[1]:
        return m
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


def signal_to_morse_text(mean_squared_amp):
    threshold = find_threshold(mean_squared_amp)
    on_off_buffer = convert_to_on_off(mean_squared_amp, threshold)
    time_unit = find_time_unit(on_off_buffer)
    return {
        "threshold": threshold,
        "time_unit": time_unit,
        "morse_text": "".join(
            morse_element(v, duration, time_unit) for v, duration in on_off_buffer
        ).strip(),
    }


def soundfile_to_morse_text(filename):
    channels, rate = load_file(filename)
    mean_squared_amp_arr = [
        windowed_mean_squared_amplitude(ch, rate) for ch in channels
    ]
    mean_squared_amp = np.mean(mean_squared_amp_arr, axis=0)
    return signal_to_morse_text(mean_squared_amp)


def soundfile_to_text(filename):
    data = soundfile_to_morse_text(filename)
    data["text"] = decode(data["morse_text"])
    return data