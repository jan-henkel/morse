morse_table = r"""A	.-	B	-...	C	-.-.	D	-..	E	.	F	..-.
G	--.	H	....	I	..	J	.---	K	-.-	L	.-..
M	--	N	-.	O	---	P	.--.	Q	--.-	R	.-.
S	...	T	-	U	..-	V	...-	W	.--	X	-..-
Y	-.--	Z	--..
0	-----	1	.----	2	..---	3	...--	4	....-	5	.....
6	-....	7	--...	8	---..	9	----.
.	.-.-.-	,	--..--	?	..--..	'	.----.	!	-.-.--	/	-..-.
(	-.--.	)	-.--.-	&	.-...	:	---...	;	-.-.-.	=	-...-
+	.-.-.	-	-....-	_	..--.-	"	.-..-.	$	...-..-	@	.--.-.
¿	..-.-	¡	--...-"""
morse_table = morse_table.replace("\t", " ").replace("\n", " ").split(" ")
characters = [c for i, c in enumerate(morse_table) if i % 2 == 0]
codes = [c for i, c in enumerate(morse_table) if i % 2 == 1]
morse_mapping = dict(zip(characters, codes))
inverse_morse_mapping = dict(zip(codes, characters))


def encode(x):
    words = x.upper().split()
    words_encoded = [
        list(map(lambda letter: morse_mapping.get(letter, ""), word)) for word in words
    ]
    return "   ".join(" ".join(word) for word in words_encoded)


def decode(x):
    words = x.split("  ")
    words = [word.strip().split() for word in words]
    words_decoded = [
        list(map(lambda letter: inverse_morse_mapping.get(letter, ""), word))
        for word in words
    ]
    return " ".join("".join(word) for word in words_decoded)


if __name__ == "__main__":
    print("Enter 1 to encode, 2 to decode: ")
    mode = int(input())
    if mode == 1:
        print("Enter phrase: ")
        phrase = input()
        print("Encoded:", encode(phrase))
    else:
        print("Enter encoded phrase: ")
        phrase = input()
        print("Decoded:", decode(phrase))
