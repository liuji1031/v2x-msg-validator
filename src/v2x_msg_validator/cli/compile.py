import glob
import os
from typing import Annotated
import logging
from pathlib import Path

import typer
from pycrate_asn1c.asnproc import compile_text
from pycrate_asn1c.generator import PycrateGenerator

import v2x_msg_validator.log_config

logger = logging.getLogger(__name__)

app = typer.Typer()


def compile_asn_folder(input_folder: str, output_path: str):
    """
    Compiles all .asn files in a folder into a single Python file.

    Args:
        input_folder [str]: folder containing the asn files
        output_path [str]: full path to the output python file
    """
    # collect all ASN.1 files in the directory
    asn_files = glob.glob(os.path.join(input_folder, "*.asn"))
    asn_files += glob.glob(os.path.join(input_folder, "*.asn1"))

    asn_text = ""
    for filename in asn_files:
        with open(filename, "r", encoding="latin-1") as f:
            asn_text += f.read() + "\n"

    # compile the text, the output is stored internally in GLOBAL variable
    # inside pycrate
    compile_text(asn_text)

    # generate Python source code
    PycrateGenerator(output_path)


@app.command()
def main(
    input_folder: Annotated[
        Path,
        typer.Option(
            "--input-folder",
            "-i",
            help="Path to the folder containing ASN.1 files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Option(
            "--output-path",
            "-o",
            help="Path of the output Python file (path + <filename>.py)",
            dir_okay=False,
        ),
    ],
):  
    if not output_path.parent.exists():
        logger.warning("Parent path of output file %s does not exist, creating...", str(output_path))
        output_path.parent.mkdir(parents=True, exist_ok=True)
    compile_asn_folder(input_folder=str(input_folder), output_path=str(output_path))
    logger.info("Compilation completed, output file: %s", str(output_path))


if __name__ == "__main__":
    app()
