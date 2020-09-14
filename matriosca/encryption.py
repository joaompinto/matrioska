from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
from pathlib import Path
from sys import stderr, stdin, stdout
from os import environ


def check_key_value(key_env):
    try:
        key_value = environ[key_env]
    except KeyError:
        print(f"ERROR: Environment var {key_env} is not defined", file=stderr)
        exit(2)
    bin_key_value = b64decode(key_value)
    if len(bin_key_value) != 32:
        print(
            f"ERROR: Value provided at {key_env} is not at 32 bytes value", file=stderr
        )
        exit(2)
    return bin_key_value


def encrypt(
    input_filename: str, output_filename: str, force: bool, encryption_key=None
):
    def write_to_file(output_file, nonce, tag, ciphertext):
        output_file.write(b"AES256")
        output_file.write(nonce)
        output_file.write(tag)
        output_file.write(ciphertext)

    if encryption_key:
        key = encryption_key
    else:
        key = get_random_bytes(32)  # AES256
    plain_key = b64encode(key).decode()

    cipher = AES.new(key, AES.MODE_EAX)
    if input_filename:
        with open(input_filename, "rb") as input_file:
            data = input_file.read()
    else:
        data = stdin.buffer.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)

    if not encryption_key and stdout.isatty():
        print(f"Encryption key: {plain_key}")

    if output_filename:
        if Path(output_filename).exists() and not force:
            print(f"{output_filename} already exists!", file=stderr)
            exit(1)
        if stdout.isatty():
            print(f" Encryped file: {output_filename}")

        with open(output_filename, "wb") as output_file:
            write_to_file(output_file, cipher.nonce, tag, ciphertext)
    else:
        if stdout.isatty():
            print("*** Encrypted content ***")
            print(b64encode(b"AES256").decode(), end="")
            print(b64encode(cipher.nonce).decode(), end="")
            print(b64encode(tag).decode(), end="")
            print(b64encode(ciphertext).decode())
            print("*************************")
        else:
            if not encryption_key:
                print(
                    "ERROR: Encryption key env name must be provided using -k",
                    file=stderr,
                )
                exit(2)
            write_to_file(stdout.buffer, cipher.nonce, tag, ciphertext)


def decrypt(
    input_filename: str, output_filename: str, force: bool, encryption_key=None
):
    if not encryption_key:
        print("ERROR: Encryption key env name must be provided using -k", file=stderr)
        exit(2)
    pass
