# Changelog

## 1.0 - 21.01.2023

### Added
- Main functionality: rename files in directory to their hash string value
- `--algorithm <algorithm>` argument to specify hash algorithm to use. Supported: md5, sha256, sha512, sha1, sha3_256, sha3_512, blake2b, blake2s 
- `--dry` run support to run without changing any file
- `--patterns <patterns>` argument to specify patterns to scan
- `--quick` run support to skip file names that look correct 
- `--size` to set the digest size. Works only for blake2b and blake2s 
- `--verbose` to enable verbose output 
- `--version` to print version info