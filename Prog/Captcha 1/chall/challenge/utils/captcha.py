from random import randint, choice


def generate() -> tuple[str, str]:
    a, b = sorted([randint(5,20) for _ in range(2)], reverse=True)
    op = choice('+-')
    if op == '+':
        code = a + b
    elif op == '-':
        code = a - b
    code = str(code)
    captcha = f'{a} {op} {b}'
    return code, captcha