import random
import time
from os import environ as env

FLAG = env.get("FLAG", "An error occured. Please contact admins.")

print("""Welcome to CyberNight!
This is a simple challenge to introduce you to programming challenges.

Example:
Input: Hello World
Output: dlroW olleH""")


def generate_word(length):
    return "".join([chr(random.randint(97, 122)) for _ in range(length)])


def reverse_word(word):
    return word[::-1]


def main():
    default_words = ["kayak", "Efrei Paris", "Salut les écureuils"]
    random_words = [generate_word(12), generate_word(15), generate_word(20)]
    words = default_words + random_words
    for word in words:
        print("> " + word + "\n< ", end="")
        t1 = time.time()
        response = input()
        t2 = time.time()
        if response == reverse_word(word) and t2 - t1 < 5:
            print("Correct!\n")
        elif t2 - t1 >= 5:
            print("Too slow! Try again.")
            return False
        else:
            print("Incorrect! Try again.")
            return False
    print("Congrats! The flag is " + FLAG)
    return True


if __name__ == "__main__":
    main()
