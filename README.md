# renash

renash is a command-line tool for renaming files based on their hash digest value.  
It supports various hash algorithms such as MD5, SHA256, SHA512, SHA1, SHA3_256, SHA3_512, BLAKE2B, and BLAKE2S.

## Installation

There is currently one option for installing renash.

Using the provided shell script (unix):

```shell
./install.sh
```

This will create a symbolic link of the renash.py command to the `~/.local/bin` directory,
making it available for the current user.

## Uninstallation

To uninstall renash, you can use the provided shell script:

```shell
./uninstall.sh
```

This will remove the symbolic link of the renash.py command from the ~/.local/bin directory.

## Usage

```shell
renash --patterns "*.jpg,*.mp4" --algorithm sha256 --dry --quick --verbose
```

### Parameters

```
[--algorithm <algorithm>]: Sets the hash algorithm. Available: 'md5', 'sha256', 'sha512', 'sha1', 'sha3_256', 'sha3_512', 'blake2b', 'blake2s'. Default is 'sha256'
[--dry]: Dry run. Only prints information about what would be done
[--patterns <patterns>]: A comma-separated string of file name glob patterns. Example: "*.jpg,*.mp4"
[--quick]: Quick run. Skips files that look already properly named
[--size <size>]: Sets the digest length to use. Works only for algorithms blake2b and blake2s
[--verbose]: Print output verbosely
[--version]: Print version
```

### Example

For example, to rename all jpeg and mp4 files in the current directory to their sha256 hash value:

```shell
renash --patterns "*.jpg,*.mp4" --algorithm sha256
```

## Note

Use this tool with caution, as it may cause data loss if used improperly.
Make sure to back up your files before using this tool.

## Contribution

We welcome contributions from the community.  
Feel free to open an issue or submit a pull request.

## License

[GPLv3](LICENSE)