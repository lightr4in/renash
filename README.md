# renash

renash is a command-line tool for renaming files based on their hash digest value.  
It supports various hash algorithms such as MD5, SHA256, SHA512, SHA1, SHA3_256, SHA3_512, BLAKE2B, and BLAKE2S.

## Installation

There is currently one option for installing renash.

Using the provided shell script (unix):

```shell
git clone https://codeberg.org/lightrain/renash.git
cd renash
./install.sh
```

This will create a symbolic link of the renash command to the `~/.local/bin` directory,
making it available for the current user.

## Uninstallation

To uninstall renash, you can use the provided shell script:

```shell
./uninstall.sh
```

This will remove the symbolic link of the renash command from the \``~/.local/bin` directory.

## Hash Algorithms

The following hash algorithms are currently supported

| Name       | Digest Size (bytes) | Digest size |
|------------|---------------------|-------------|
| `md5`      | 16                  | fixed       |
| `sha256`   | 32                  | fixed       |
| `sha512`   | 64                  | fixed       |
| `sha1`     | 20                  | fixed       |
| `sha3_256` | 32                  | fixed       |
| `sha3_512` | 64                  | fixed       |
| `sha3_512` | 64                  | fixed       |
| `blake2b`  | <= 64               | variable    |
| `blake2s`  | <= 32               | variable    |

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

## Example

For example, to rename all jpg and mp4 files in the current directory to their sha256 hash value:

```shell
renash --patterns "*.jpg,*.mp4"
```

### Dry Mode

Be sure to always use `--dry` switch to output all persistent file operations that would be executed without the switch.

For instance, list all file changes _(any file)_ that would be made in the current directory:

```shell
renash --dry
```

### Quick Mode

The `--quick` switch allows ignoring files that look properly named i.e. like if they would have already been processed.

For example, to rename all jpg files in the current directory to their sha256 hash value in quick mode:

```shell
renash --quick --patterns "*.jpg"
```

### Custom Digest Size

To [customize the output digest size](#hash-algorithms), you must use either `blake2b` or `blake2s` as hashing algorithm.

For instance, use digest size of 20 bytes for `blake2b` algorithm:

```shell
renash --algorithm blake2b --size 20
```

## Note

Use this tool with caution, as it may cause data loss if used improperly.  
Make sure to back up your files before using this tool if in doubts.

## Contribution

We welcome contributions from the community.  
Feel free to open an issue or submit a pull request.

## License

[GPLv3](https://codeberg.org/lightrain/renash/src/branch/master/LICENSE)