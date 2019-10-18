import argparse
import os
import subprocess
import sys
from typing import List


def get_vendored_path(output: str) -> str:
    for line in output.split(os.linesep):
        if line.strip().startswith("Saved"):
            return line.strip().split(" ")[1]


def get_package_name(output: str) -> str:
    for line in output.split(os.linesep):
        if line.strip().startswith("Successfully downloaded"):
            return line.strip().split(" ")[2]


def update_reqs_txt(path: str, reqs: str):
    with open(reqs, "a") as fh:
        fh.write(f"{os.linesep}{path}{os.linesep}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="Vendor python packages with pip.")
    parser.add_argument(
        "package", metavar="PACKAGE", type=str, help="Package to vendor"
    )
    parser.add_argument(
        "--vendor_path",
        type=str,
        help="Path to vendor directory",
        default=f"{os.environ.get('PWD')}/vendor",
    )
    parser.add_argument(
        "--requirements_txt",
        type=str,
        help="Path to the requirements.txt to update",
        default="requirements.txt",
    )
    return parser


def vendor(pkg: str, vendor_dir: str, reqs: str):
    print(f"Downloading {pkg} to {vendor_dir}...")
    output = subprocess.run(
        ["pip", "download", "--dest", vendor_dir, pkg], capture_output=True
    ).stdout.decode("utf8")
    vendored_path = get_vendored_path(output)
    if not vendored_path:
        print(output)
        sys.exit(1)
    package_name = get_package_name(output)
    if not package_name:
        print(output)
        sys.exit(1)
    print(f"Adding {vendored_path} to {reqs}")
    update_reqs_txt(vendored_path, reqs)
    print(f"Vendored {package_name} in {vendored_path} and updated {reqs}")


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    vendor(args.package, args.vendor_path, args.requirements_txt)
