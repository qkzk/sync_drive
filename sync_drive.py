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

import datetime
import multiprocessing
import os
import subprocess

import yaml


CONFIG_FILE = "./config.yml"
DRIVE_PUSH_COMMAND = "drive push -ignore-name-clashes . -no-prompt"
NOTIFY_USER_COMMAND = 'notify-send "{} - sync_drive - {} - push finished"'


def load_config(filename: str = CONFIG_FILE) -> dict:
    """Load the config file"""
    with open(filename, "r", encoding="utf-8") as config:
        return yaml.load(config, Loader=yaml.Loader)


def move_to_dir(directory: str) -> None:
    """Move into a directory."""
    os.chdir(directory)


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
    return (
        "" if result.stdout is None else result.stdout.read().decode("utf-8"),
        "" if result.stderr is None else result.stderr.read().decode("utf-8"),
    )


def notify(directory: str) -> None:
    """Notify a user with datetime and directory name."""
    cmd = NOTIFY_USER_COMMAND.format(
        datetime.datetime.now().strftime("%H:%M"), directory
    )
    run_command(cmd)


def push_dir_to_drive(directory: str):
    """Move into a directory and run the drive push command."""
    move_to_dir(directory)
    run_command(DRIVE_PUSH_COMMAND)
    notify(directory)


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
    config = load_config()
    print(config)
    push_all_dir(config)


if __name__ == "__main__":
    main()
