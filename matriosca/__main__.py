from .argparser import arg_parser
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode
from pathlib import Path
from sys import stderr


def main():
    options, args = arg_parser()
    input_filename = args[0]
    key = get_random_bytes(32)  # AES256
    plain_key = b64encode(key).decode()

    cipher = AES.new(key, AES.MODE_EAX)
    with open(input_filename, "rb") as input_file:
        data = input_file.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)

    output_filename = input_filename + ".aes256"
    if Path(output_filename).exists():
        print(f"{output_filename} already exists!", file=stderr)
        exit(1)

    with open(output_filename, "wb") as output_file:
        output_file.write(b"AES256")
        output_file.write(cipher.nonce)
        output_file.write(tag)
        output_file.write(ciphertext)
    print(f"Encryption key: {plain_key}")
    print(f" Encryped file: {output_filename}")


if __name__ == "__main__":
    main()
