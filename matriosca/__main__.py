from .argparser import arg_parser
from .encryption import encrypt, decrypt, check_key_value


def main():
    options, args = arg_parser()
    input_filename = None
    output_filename = None
    encryption_key = None
    if options.key_env:
        encryption_key = check_key_value(options.key_env)
    if len(args) == 1:
        input_filename = args[0]
    if options.decrypt:
        if input_filename:
            output_filename = input_filename.replace(".aes256", "")
        decrypt(
            input_filename,
            output_filename,
            force=options.force,
            encryption_key=encryption_key,
        )
    else:
        if input_filename:
            output_filename = input_filename + ".aes256"
        encrypt(
            input_filename,
            output_filename,
            force=options.force,
            encryption_key=encryption_key,
        )


if __name__ == "__main__":
    main()
