from morse import morse_text_processing, morse_audio_encode, morse_audio_decode
import argparse

parser = argparse.ArgumentParser()
mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument("--plaintext", metavar="TEXT", help="Set plain text")
mode_group.add_argument("--morsetext", metavar="TEXT", help="Set morse text")
mode_group.add_argument(
    "--morseaudio", metavar="FILE", help="Set morse audio file name"
)
parser.add_argument(
    "--verbose",
    help="Show additional information",
    action="store_const",
    const=True,
    default=False,
)
parser.add_argument(
    "--playaudio",
    help="Play morse code audio",
    action="store_const",
    const=True,
    default=False,
)
parser.add_argument(
    "--saveaudio",
    metavar="FILE",
    help="Name of morse code audio file to be written",
)

args = parser.parse_args()
if args.plaintext:
    plain_text = args.plaintext
    morse_text = morse_text_processing.encode(args.plaintext)

if args.morsetext:
    plain_text = morse_text_processing.decode(args.morsetext)
    morse_text = args.morsetext

if args.morseaudio:
    data = morse_audio_decode.process_soundfile(args.morseaudio)
    plain_text = data["plain_text"]
    morse_text = data["morse_text"]

print("Plain text", plain_text)
print("Morse text", morse_text)

if args.morseaudio is None:
    if args.playaudio or args.saveaudio:
        audio_buffer = morse_audio_encode.morse_text_to_audio_buffer(morse_text)
    if args.playaudio:
        morse_audio_encode.play_audio_buffer(audio_buffer)
    if args.saveaudio:
        morse_audio_encode.save_audio_buffer(audio_buffer, args.saveaudio)

if args.morseaudio and args.verbose:
    print("Squared amplitude threshold", data["threshold"])
    print("Time unit (in seconds)", data["time_unit"])