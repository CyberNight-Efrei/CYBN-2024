from hashlib import md5
from random import randint
import strings
import os


def print_center(msg):
    for line in msg.splitlines():
        print(line.center(strings.MAX_STRING_WIDTH))


def generate_id():
    return randint(10**6, 10**7-1)


def compute_key(account_id):
    key = str(account_id).encode()
    for _ in range(30):
        key = md5(key).digest()
    return key.hex()


def login(account_id: int):
    if account_id not in ACCOUNTS:
        print_center(strings.LOGIN_NOT_FOUND)
        return
    print_center(strings.LOGIN_KEY.format(account_id=account_id))
    key = input('\n> ')
    if key == compute_key(account_id):
        print_center(strings.LOGIN_SUCCESS)
        if account_id == ADMIN_ID:
            print_center(strings.LOGIN_SUCCESS_ADMIN.format(flag=FLAG))
        else:
            print_center(strings.LOGIN_SUCCESS_ANONYMOUS)
    else:
        print_center(strings.LOGIN_FAIL)
    exit()


def register():
    if len(ACCOUNTS) >= 5:
        print_center(strings.REGISTER_LIMIT)
        return

    while True:
        account_id = randint(50, 2000)
        if account_id not in ACCOUNTS:
            break
    ACCOUNTS.append(account_id)
    key = compute_key(account_id)
    print_center(strings.REGISTER.format(account_id=account_id, key=key))


def credits():
    print_center(strings.CREDITS.format(admin=ADMIN_ID))


def main():
    print_center(strings.BANNER)
    while True:
        print_center(strings.MENU)
        choice = input('\n> ').strip()
        if choice == 'register':
            register()
        elif choice == 'credits':
            credits()
        else:
            try:
                login(int(choice))
            except Exception:
                pass
            


ADMIN_ID = generate_id()
ACCOUNTS = [ADMIN_ID]
FLAG = os.environ.get('FLAG', 'CYBN{REDACTED}')

if __name__ == '__main__':
    main()
