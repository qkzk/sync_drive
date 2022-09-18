#!/usr/bin/python
"""
title: sync google drive with `drive` command
author: qkzk
date: 2022/06/19

Linux doesn't have a native google drive client.
Among many options, [drive](https://github.com/odeke-em/drive) is the one I chosed.
Drive uses directory config files, allowing multiple accounts on the same computer.

This script will read paths to push from a `config.yaml` file in same directory.
It will then push every directory as subprocess.
"""

from typing import IO, Optional
import datetime
import multiprocessing
import os
import subprocess

import yaml


CONFIG_FILE = "./config.yml"
DRIVE_PUSH_COMMAND = "drive push -ignore-name-clashes -no-prompt ."
NOTIFY_USER_COMMAND = "notify-send {}"


def load_config(filename: str = CONFIG_FILE) -> dict:
    """Load the config file"""
    with open(filename, "r", encoding="utf-8") as config:
        return yaml.load(config, Loader=yaml.Loader)


def move_to_dir(directory: str) -> None:
    """Move into a directory."""
    os.chdir(directory)


def parse_output(output: Optional[IO[bytes]]) -> str:
    """
    Parse the output (stdout or stderr) or a command into a string.
    Returns an empty string the output is None
    """
    return "" if output is None else output.read().decode("utf-8")


def run_command(command: str) -> tuple[str, str]:
    """
    Run the command.
    Returns a tuple with stdout and stderr
    """
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    return parse_output(result.stdout), parse_output(result.stderr)


def format_welcome_message() -> str:
    """Format a welcome message with datetime"""
    return f"sync_drive started : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"


def format_completed_message(directory: str) -> str:
    """Format a completed message"""
    return "{} - sync_drive - {} - push finished".format(
        datetime.datetime.now().strftime("%H:%M"), directory.split("/")[-1]
    )


def notify(message: str) -> None:
    """Notify a user with datetime and directory name."""
    print(message)
    run_command(NOTIFY_USER_COMMAND.format(message))


def push_dir_to_drive(directory: str):
    """Move into a directory and run the drive push command."""
    move_to_dir(directory)
    run_command(DRIVE_PUSH_COMMAND)
    notify(format_completed_message(directory))


def push_all_dir(config: dict[str, str]):
    """
    For every dir, push it to drive.
    Run as a separate process in a pool.
    The pool size is as big as necessary ie. min of config size and cpu_count.
    """
    pool_size = min(multiprocessing.cpu_count(), len(config))
    pool = multiprocessing.Pool(pool_size)
    pool.map(push_dir_to_drive, config.values())


def main():
    """
    Main program.
    Load directories from the config file,
    For every directory, cd into it and run the command.
    """
    notify(format_welcome_message())
    config = load_config()
    print(config)
    push_all_dir(config)


if __name__ == "__main__":
    main()
