from optparse import OptionParser
from .version import version


def arg_parser():
    parser = OptionParser(version=version)
    parser.add_option(
        "-d",
        "--decrypt",
        action="store_true",
        dest="decrypt",
        default=False,
        help="decrypt file",
    )
    parser.add_option(
        "-k",
        "--key-env",
        action="store",
        dest="key_env",
        default=None,
        help="environment variable name containing the encryption key",
    )
    parser.add_option(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        default=False,
        help="overwrite output file if it exists",
    )
    (options, args) = parser.parse_args()
    return (options, args)
