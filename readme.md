# Introduction
This script is a Morse encoder / decoder with audio and text processing features.
# Prerequisites
To be able to use this script, the following is required:
* Python 3
* NumPy
* simpleaudio
* pydub
* ffmpeg (optional, required for non-wav audio input)
# Usage
Call `python main.py` using some of the following arguments
```
usage: main.py [-h] (--plaintext TEXT | --morsetext TEXT | --morseaudio FILE) [--verbose] [--playaudio] [--saveaudio FILE]

optional arguments:
  -h, --help         show this help message and exit
  --plaintext TEXT   Set plain text
  --morsetext TEXT   Set morse text
  --morseaudio FILE  Set morse audio file name
  --verbose          Show additional information
  --playaudio        Play morse code audio
  --saveaudio FILE   Name of morse code audio file to be written
```
The `--plaintext`, `--morsetext` and `--morseaudio` arguments are mutually exclusive, as they describe the input to be processed.
## Morse code notation
Morse code input and output is expected and provided respectively in "dot-dash"-notation, wherein:
* \. denotes a dot
* \- denotes a dash
* Dots and dashes describing one letter have no spaces between them
* Individual letters are separated by one space
* Words are separated by 3 spaces
## Text input processing
Passing plain text input is simply done via `--plaintext "[some text]"`.  
Morse code is passed using `--morsetext "[morse code]"` where `[morse code]` is given in dot-dash notation described above.

Setting either one will yield console output with both plain text and the corresponding Morse code in dot-dash notation.

Passing `--playaudio` will yield Morse code audio.

Setting `--saveaudio "[file name].wav"` will save Morse code audio in a `wav` file.
## Audio input processing
An audio file can be processed by setting `--morseaudio "[file name]"`. Note that non-`wav` input requires `ffmpeg`.

Again, the console output will show both Morse code extracted from the audio as well as decoded plain text.

Passing `--verbose` shows additional information, such as how long a "time unit" (the duration of a dot) was deemed to be as well as the threshold level for the signal to be considered "on".
# Technical details
Text processing is done in [morse_text_processing.py](morse/morse_text_processing.py) and relies on 2 dictionaries mapping plain text to "dot-dash" notation and vice-versa.

Audio encoding is done in [morse_audio_encode.py](morse/morse_audio_encode.py).  
The central function, `morse_text_to_audio_buffer`, works as follows:
* Morse code text is re-encoded by replacing (empty) inter-element gaps by "e", gaps between letters with "l" and gaps between words with "w"
* Dots, dashes and the aforementioned gap-characters are translated to corresponding audio buffers, containing either a sine wave or a pause of the appropriate length
* The audio buffers are then concatenated

Audio decoding, which is a little more tricky, is done in [morse_audio_decode.py](morse/morse_audio_decode.py).  
The central function, `process_signal`, works as follows:
* The audio signal is turned into a sequence of values denoting the "loudness" within non-overlapping windows / intervals of a given length. For the time being this is just the mean squared amplitude over the given windows
* A threshold value for the signal to be considered "on" is selected from the sequence. At the moment this is simply the mean
* Consecutive "on" and "off" states are grouped together and paired up with their length
* A time unit (the duration of a dot) is extracted from the durations. At the moment this is taken to be the average of the median and minimum duration, or a default value if this falls outside of a range of reasonable values
* Using the time unit, the on-off signal is now mapped to dots, dashes and appropriately sized gaps