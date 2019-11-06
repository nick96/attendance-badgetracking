import argparse
import getpass
import os
import sys

import docker
from docker import errors
from docker.models.containers import Container


def update_password(container_name: str, user: str, old_pass: str, new_pass: str):
    client = docker.from_env()
    try:
        container: Container = client.containers.get(container_name)
    except errors.NotFound as err:
        print(f"Could not find container {container_name}: {str(err)}")
        sys.exit(1)
    rv, _ = container.exec_run(
        ["psql", "-U", user, "-c", r"\password", new_pass],
        environment={"PGPASSWORD": old_pass},
    )
    if rv != 0:
        print(
            f"Failed to update postgres password for user {user} on container {container_name}"
        )
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update postgres database password in a docker container"
    )
    parser.add_argument(
        "--container_name", type=str, help="Name of the container running postgres"
    )
    parser.add_argument(
        "--user", type=str, help="Name of the user who's password we're updating"
    )
    parser.add_argument(
        "--old_password",
        type=str,
        help="Old password",
        default=os.environ.get("OLD_PASSWORD", ""),
    )
    parser.add_argument(
        "--new_password",
        type=str,
        help="New password",
        default=os.environ.get("NEW_PASSWORD", ""),
    )
    args = parser.parse_args()
    if not args.old_password:
        args.old_password = getpass.getpass("Old password: ")
    if not args.new_password:
        args.new_password = getpass.getpass("New password: ")
    update_password(
        args.container_name, args.user, args.old_password, args.new_password
    )
