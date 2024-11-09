from argparse import ArgumentParser

from imagescript.converter import Converter

__version__ = "0.1.0"

def main():
    parser = ArgumentParser(
        prog="imagescript",
        description="A command line tool to convert text into images and back. Also supports executing images as "
                    "scripts and basic Steganography with pack and unpack."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"ImageScript v{__version__}",
        help="Print the version number and exit.",
    )
    subparsers = parser.add_subparsers(title="command", help="The command to execute.", required=True, dest="command")

    subparsers.add_parser("to_image", help="Convert text to an image.")

    subparsers.add_parser("to_text", help="Convert image to a text.")

    subparsers.add_parser("unpack", help="Extract text from an image file.")

    subparsers.add_parser("pack", help="Pack a text file into an image. (Steganography)")

    subparsers.add_parser(
        "execute", help="Execute an image file containing a python script. (Steganography)"
    )

    args = parser.parse_args()
    match args.command:
        case "to_image":
            Converter.file_to_image()

if __name__ == "__main__":
    main()
