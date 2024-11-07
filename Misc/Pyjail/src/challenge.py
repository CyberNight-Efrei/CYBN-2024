#!/usr/bin/env python3


def check_code(code: str) -> str:
    allowed_chars = ('"', "+", "c", "%", "<", "(", ")")

    for c in code:
        if c not in allowed_chars:
            return c

    return None


if __name__ == "__main__":
    code = input(">>> ")

    if (invalid := check_code(code)) is None:
        exec(eval(code))
    else:
        print(f"Nahh, your entered '{invalid}' and it scares me...")
