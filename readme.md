## sync google drive with `drive` command

Linux doesn't have a native google drive client.
Among many options, [drive](https://github.com/odeke-em/drive) is the one I chosed.
Drive uses directory config files, allowing multiple accounts on the same computer.

This script will read paths to push from a `config.yaml` file in same directory.
It will then push every directory as subprocess.

## Installation

1. install drive (see link above)
2. configure drive for your multiple folders (see drive help)
3. make sure to have `notify-send` installed. It's included in many user friendly linux distributions.
