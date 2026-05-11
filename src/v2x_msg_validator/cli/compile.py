import glob
import logging
import os
import subprocess
from pathlib import Path
from typing import Annotated

import typer
import v2x_msg_validator.logger_config
from pycrate_asn1c.asnproc import compile_text
from pycrate_asn1c.generator import PycrateGenerator

logger = logging.getLogger(__name__)

app = typer.Typer()

SRC_ROOT = Path(__file__)
iter = 0
max_iter = 5
while SRC_ROOT.name != "src":
    SRC_ROOT = SRC_ROOT.parent
    iter += 1
    if iter > max_iter:
        break
if SRC_ROOT.name != "src":
    # if cannot find src, reset
    SRC_ROOT = Path(__file__)


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


def setup_compiled_package_uv() -> None | Path:
    """Create a subpackage for compiled code using uv.

    Assuming uv is installed, use `uv init --bare` to create the package.
    If
    """
    local_package_path = SRC_ROOT / ".compiled"
    subpackage_name = "v2x_codecs"

    if not local_package_path.exists():
        logger.info("Creating .compiled folder at %s", str(local_package_path))
        local_package_path.mkdir(parents=True, exist_ok=True)

    if (local_package_path / subpackage_name / "__init__.py").exists():
        logger.info("Local package already set up, skipping...")
        return local_package_path / subpackage_name

    try:
        if not local_package_path.exists():
            local_package_path.mkdir(parents=True)
        subprocess.run(
            [
                "uv",
                "init",
                "--bare",
                "--name",
                subpackage_name,
                "--build-backend",
                "hatch",
            ],
            cwd=local_package_path,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(["uv", "add", "pycrate", "--no-sync"])
        logger.info(
            "Successfully set up local package at %s", str(local_package_path)
        )
    except Exception as e:
        logger.error("Error during local package creation: %s", e)
        return None

    # create the package structure
    subpackage_path = local_package_path / subpackage_name
    try:
        subpackage_path.mkdir(parents=True, exist_ok=True)
        (subpackage_path / "__init__.py").touch(exist_ok=True)
        subprocess.run(
            ["uv", "add", "--editable", ".compiled"],
            cwd=SRC_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        logger.error("Error during local package installation: %s", e)
        return

    return subpackage_path  # where to dump all future compiled files


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
    module_name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="The name of the compiled module (without .py)",
        ),
    ],
):
    module_name = module_name if module_name.endswith(".py") else module_name + ".py"

    # install the local package
    subpackage_path = setup_compiled_package_uv()

    if subpackage_path is None:
        return

    output_file_path = str(subpackage_path / (module_name))

    compile_asn_folder(
        input_folder=str(input_folder), output_path=output_file_path
    )
    logger.info("Compilation completed, output file: %s", output_file_path)


if __name__ == "__main__":
    app()
