from morse import morse_text, morse_audio

if __name__ == "__main__":
    print("Enter 1 to encode, 2 to decode, 3 to encode and generate audio: ")
    mode = int(input())
    if mode == 1:
        print("Enter text: ")
        text = input()
        print("Encoded:", morse_text.encode(text))
    elif mode == 2:
        print("Enter encoded text: ")
        text = input()
        print("Decoded:", morse_text.decode(text))
    elif mode == 3:
        print("Enter text: ")
        text = input()
        morse_audio.morse_beep(text)