#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from typing import List, Generator


def get_vendored_paths(output: str) -> List[str]:
    paths = []
    for line in output.split(os.linesep):
        if line.strip().startswith("Saved"):
            vendored_path = line.strip().split(" ")[1]
            paths.append(vendored_path)
    return paths


def get_package_names(output: str) -> List[str]:
    names = []
    for line in output.split(os.linesep):
        if line.strip().startswith("Collecting"):
            package_name = line.strip().split(" ")[1]
            names.append(package_name)
    return names


def update_reqs_txt(path: str, reqs: str):
    with open(reqs, "a") as fh:
        fh.write(f"{os.linesep}{path}{os.linesep}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="Vendor python packages with pip.")
    parser.add_argument(
        "packages", metavar="PACKAGES", type=str, nargs="+", help="Packages to vendor"
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
    parser.add_argument(
        "--no_install",
        action="store_true",
        help="Do not install the vendored package(s)",
    )
    return parser


def vendor(pkgs: List[str], vendor_dir: str, reqs: str, install: bool):
    print(f"Downloading {pkgs} to {vendor_dir}...")
    cmd = ["pip", "download", "--dest", vendor_dir, *pkgs]
    output = subprocess.run(cmd, capture_output=True).stdout.decode("utf8")

    vendored_paths = get_vendored_paths(output)
    if not vendored_paths:
        print(output)
        sys.exit(1)

    package_names = get_package_names(output)
    if not package_names:
        print(output)
        sys.exit(1)

    for vendored_path, package_name in zip(vendored_paths, package_names):
        update_reqs_txt(vendored_path, reqs)
        print(f"Vendored {package_name} in {vendored_path} and updated {reqs}")

    if install:
        print(f"Installing packages...")
        subprocess.run(["pip", "install", "-r", reqs])


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    vendor(args.packages, args.vendor_path, args.requirements_txt, not args.no_install)
