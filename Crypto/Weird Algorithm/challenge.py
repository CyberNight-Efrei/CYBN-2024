import itertools

import numpy as np
import sympy as sp


def encode(string: str, first: str, second: str) -> str:
    chars = (first, second)
    cleaned_string = string.replace(" ", chr(1))

    letters = np.array(
        [
            sp.factorint(ord(letter), multiple=True)
            for letter in cleaned_string
        ],
        dtype=object,
    )

    depth = max([len(i) for i in letters])

    cleaned_letters = []

    for primes in letters:
        if len(primes) == depth:
            cleaned_letters.append(np.random.permutation(primes))
        else:
            cleaned_letters.append(
                np.random.permutation(
                    [1 for _ in range(depth - len(primes))] + list(primes)
                )
            )

    cleaned_letters = np.array(cleaned_letters, dtype=object)

    bits = int(np.amax(cleaned_letters)).bit_length()

    output = ""

    xor_key = (
        "".join(
            np.random.choice(chars)
            for _ in range(bits)
        )
    )

    print(f"{xor_key=}")


    chunks = [
        np.array(list(group), dtype=object)
        for key, group in itertools.groupby(
            cleaned_letters, key=lambda p: np.prod(p) == 1
        )
        if not key
    ]

    for chunk in np.array(chunks, dtype=object):
        layers = np.hsplit(chunk, depth)

        for layer in layers:
            for element in layer:
                binary = (
                    np.binary_repr(element[0])
                    .replace("0", chars[0])
                    .replace("1", chars[1])
                )

                padded_binary = str(chars[0] * (bits - len(binary))) + binary  # elem

                output += "".join([chars[0] if ord(padded_binary[i]) ^ ord(xor_key[i]) == 0 else chars[1] for i in range(bits)])

    return output


def decode(string: str, *args, **kwargs) -> str:
    return "uhhhhh"


if __name__ == "__main__":
    user_input = input("Your text to encode: ")
    user_first, user_second = input("Secret char A: "), input(
        "Secret char B: "
    )

    encoded_text = encode(user_input, user_first, user_second)

    with open("flag.enc", "w") as f:
        f.write(encoded_text)
