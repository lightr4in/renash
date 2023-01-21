#!/usr/bin/python3

import argparse
import os
import hashlib
import glob
import re
from enum import Enum
from typing import Optional, Callable, AnyStr, Tuple, Pattern


class HashAlgorithm(Enum):
    """
    Enumeration class for supported hash algorithms.
    """
    MD5 = 'md5'
    SHA256 = 'sha256'
    SHA512 = 'sha512'
    SHA1 = 'sha1'
    SHA3_256 = 'sha3_256'
    SHA3_512 = 'sha3_512'
    BLAKE2B = 'blake2b'
    BLAKE2S = 'blake2s'


hash_algorithms = {
    HashAlgorithm.MD5.value: {'hasher': hashlib.md5, 'length': 16},
    HashAlgorithm.SHA256.value: {'hasher': hashlib.sha256, 'length': 32},
    HashAlgorithm.SHA512.value: {'hasher': hashlib.sha512, 'length': 64},
    HashAlgorithm.SHA1.value: {'hasher': hashlib.sha1, 'length': 20},
    HashAlgorithm.SHA3_256.value: {'hasher': hashlib.sha3_256, 'length': 32},
    HashAlgorithm.SHA3_512.value: {'hasher': hashlib.sha3_512, 'length': 64},
    HashAlgorithm.BLAKE2B.value: {'hasher': hashlib.blake2b, 'length': 64, 'variable_length': True},
    HashAlgorithm.BLAKE2S.value: {'hasher': hashlib.blake2s, 'length': 32, 'variable_length': True},
}


class StatsService:
    """
    Class to store statistics of the process.
    """

    stats = {
        'processed': 0,
        'skipped': 0,
        'error': 0,
    }

    @staticmethod
    def get_error_count() -> int:
        """
        Returns the errors occurred while processing
        :return: The errors occurred (int)
        """
        return StatsService.stats['error']

    @staticmethod
    def get_formatted(dry: bool) -> str:
        """
        Returns all statistics as formatted string.
        :return: The statistics formatted as string (str)
        """
        self = StatsService
        return f"{'Processed' if dry else 'Renamed'}: {self.get_processed_count()} " \
               f"Skipped: {self.get_skipped_count()} " \
               f"Errors: {self.get_error_count()} - " \
               f"Total files: {self.sum_stats()}"

    @staticmethod
    def get_processed_count() -> int:
        """
        Returns the number of processed files
        :return: The number of processed files (int)
        """
        return StatsService.stats['processed']

    @staticmethod
    def get_skipped_count() -> int:
        """
        Returns the number of skipped files
        :return: The number of skipped files (int)
        """
        return StatsService.stats['skipped']

    @staticmethod
    def increment_error_count():
        """
        Stores the information that an error occurred while processing a file
        """
        StatsService.stats['error'] += 1

    @staticmethod
    def increment_skipped_count():
        """
        Stores the information that a file was skipped
        """
        StatsService.stats['skipped'] += 1

    @staticmethod
    def increment_processed_count():
        """
        Stores the information that a file was successfully processed
        """
        StatsService.stats['processed'] += 1

    @staticmethod
    def sum_stats() -> int:
        """
        Returns a sum of all statistics saved
        :return: The sum of all statistics (int)
        """
        return sum(StatsService.stats.values())


class FileService:
    """
    Class to handle file IO concerning tasks.
    """

    @staticmethod
    def has_move_access(file_path: str) -> bool:
        """
        Checks and returns whether a given file can be moved or not.
        :param file_path: The file path to check (str)
        :return: Whether the user has the permission to move the file (bool)
        """
        return os.access(file_path, os.W_OK)

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path) and os.path.exists(path)

    @staticmethod
    def read_file(file_name: str) -> AnyStr or None:
        """
        Reads a file in binary mode and returns its contents
        :param file_name: The file to read (str)
        :return: The binary file content (AnyStr) or None if an error occurred
        """

        try:
            with open(file_name, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Could not read {file_name} - file not found")
        except PermissionError:
            print(f"Could not read {file_name} - permission denied")
        except Exception as e:
            print(f"Could not read {file_name} : {e}")

    @staticmethod
    def rename_file(file_name: str, new_file_name: str) -> bool:
        """
        Renames a file to a new name and returns the result
        :param file_name: The source file name (str)
        :param new_file_name: The target file name (str)
        :returns: The rename result (bool)
        """
        try:
            os.rename(file_name, new_file_name)
            return True
        except Exception as e:
            print(f"Error occurred while renaming: {e}")
        return False

    @staticmethod
    def rename_files(directory: str,
                     name_patterns: [str],
                     algorithm: HashAlgorithm,
                     digest_size: Optional[int],
                     recursive=False,
                     quick_run=False,
                     dry_run=False,
                     verbose_output=False) -> bool:
        """
        Renames files matching the specified patterns to their hash value
        :param directory: The directory to process (str)
        :param name_patterns: The glob patterns to process ([str])
        :param algorithm: The algorithm to use (HashAlgorithm)
        :param digest_size: The (output) digest byte size (Optional[int])
        :param recursive: Whether the specified directory should be processed recursively (bool)
        :param quick_run: Whether matching files should be ignored (bool)
        :param dry_run: Whether no persistent changes should be performed (bool)
        :param verbose_output: Whether output should be printed verbosely (bool)
        :returns: Whether renaming was successful (bool)
        """

        hasher = HashService.get_hasher_or_none(hash_algorithm)
        if algorithm.value not in hash_algorithms or hasher is None:
            return False

        digest_size = digest_size if HashService.is_digest_length_variable(hash_algorithm) else None
        if digest_size is not None:
            print(f"Using digest size {digest_size}")

        hash_regex = HashService.get_hash_regex_if_quick(args.quick)

        prefix = '**/' if recursive else ''
        name_patterns = [os.path.join(directory, prefix, pattern) for pattern in name_patterns]

        for pattern in name_patterns:
            for file_path in glob.glob(pattern, recursive=recursive):
                file_name = os.path.basename(file_path)

                dir_path = os.path.dirname(file_path)
                relative_directory = os.path.relpath(dir_path, directory)
                relative_source_file_name = os.path.join(relative_directory, file_name)

                if not FileService.is_file(file_path):
                    continue

                if quick_run and HashService.guess_is_hash_string(file_path, hash_regex, hash_algorithm, digest_size):
                    StatsService.increment_skipped_count()
                    if verbose_output:
                        print(f"Quick: File name {relative_source_file_name} seems already properly named. Skipping")
                    continue

                file_hash = HashService.hash_file(file_path, hasher, digest_size)
                if file_hash is None:
                    StatsService.increment_error_count()
                    print(f"Could not hash file {relative_source_file_name}. Skipping")
                    continue

                new_file_name = file_hash + os.path.splitext(file_path)[1]
                directory_name = os.path.dirname(file_path)
                new_file_path = os.path.join(directory_name, new_file_name)

                if new_file_name == file_name:
                    StatsService.increment_skipped_count()
                    if verbose_output:
                        print(f"File name {relative_source_file_name} is already properly formatted. Skipping")
                    continue

                relative_target_file_name = os.path.join(relative_directory, new_file_name)

                if not dry_run:
                    rename_successful = FileService.rename_file(file_path, new_file_path)
                    if rename_successful:
                        StatsService.increment_processed_count()
                        print(f"Renamed {relative_source_file_name} to {relative_target_file_name}")
                elif FileService.has_move_access(file_path):
                    print(f"Would rename {relative_source_file_name} to {relative_target_file_name}")
                    StatsService.increment_processed_count()
                else:
                    print(f"Could not rename {relative_source_file_name} to {relative_target_file_name}")
                    StatsService.increment_error_count()
        return True


class HashService:
    """
    Class to handle hashing concerning tasks.
    """

    @staticmethod
    def get_algorithm_name_or_default(algorithm: Optional[str]) -> str:
        """
        Returns the specified algorithm if it is not None or the default value 'sha256'
        :param algorithm: The algorithm to check (str)
        :return: The (default) algorithm (str)
        """
        return HashAlgorithm.SHA256.value if algorithm is None else algorithm

    @staticmethod
    def get_compiled_hex_regex() -> Pattern[AnyStr]:
        """
        Returns a compiled regex pattern that matches hexadecimal characters.
        :return: The compiled hex regex (Pattern[AnyStr])
        """
        return re.compile(r"^[0-9a-fA-F]+$")

    @staticmethod
    def get_digest_length_or_none(algorithm: HashAlgorithm) -> Optional[int]:
        """
        Returns the hash digest size that is output by the specified algorithm.
        :param algorithm: The specified algorithm to use (HashAlgorithm)
        :return: The size of digest (int) or None if the algorithm is not supported
        """
        result = HashService.get_supported_algorithm_or_none(algorithm)
        if result is None:
            return None
        return result['length']

    @staticmethod
    def get_hash_algorithm_or_none(algorithm: Optional[str]) -> Optional[Tuple]:
        """
        Returns the enum value of HashAlgorithm that corresponds to the specified algorithm string.
        :param algorithm: The algorithm name to search (str)
        :return: The enum value of equivalent and algorithm name used (Tuple) or None if the algorithm is not supported
        """

        if algorithm is None:
            algorithm = HashService.get_algorithm_name_or_default(algorithm)

        algorithm = algorithm.lower()
        for enum_value in HashAlgorithm:
            if algorithm == enum_value.value:
                return enum_value, algorithm
        return None, algorithm

    @staticmethod
    def get_hash_regex_if_quick(quick: bool) -> Optional[Pattern[AnyStr]]:
        """
        Compiles and returns a new regex matching hexadecimal characters if runnnig in quick mode or None otherwise
        :param quick: The quick run argument (str)
        :return: The compiled regex (Pattern[AnyStr]) or None if quick is False
        """
        if quick:
            return HashService.get_compiled_hex_regex()
        return None

    @staticmethod
    def get_hasher_or_none(algorithm: HashAlgorithm) -> Optional[Callable]:
        """
        Returns the hash function that is used for the specified algorithm.
        :param algorithm: The algorithm to use (HashAlgorithm)
        :return: The corresponding hasher function (Callable) or None if the algorithm is not supported
        """

        result = HashService.get_supported_algorithm_or_none(algorithm)
        if result is None:
            return None
        return result['hasher']

    @staticmethod
    def get_supported_algorithm_or_none(algorithm: HashAlgorithm) -> Optional[object]:
        """
        Returns the corresponding algorithm object if supported or None otherwise.
        :param algorithm: The algorithm to search (HashAlgorithm)
        :return: The algorithm object (object) or None if the algorithm is not supported
        """
        algorithm_str: str = algorithm.value
        if algorithm_str in hash_algorithms:
            return hash_algorithms[algorithm_str]
        return None

    @staticmethod
    def get_supported_hash_algorithms() -> str:
        """
        Returns a string supported hash algorithms, separated by comma and whitespace.
        :returns: comma separated string of algorithms (str)
        """
        return ", ".join([enum_value.value for enum_value in HashAlgorithm])

    @staticmethod
    def guess_is_hash_string(file_name: str, hash_regex: re, algorithm: HashAlgorithm,
                             digest_size: Optional[int]) -> bool:
        """
        Returns True if the file name looks like it is already a hash string.
        :param file_name: The file name to analyze (str)
        :param hash_regex: The hash regex allowing hex chars (re)
        :param algorithm: The hash algorithm to compare (HashAlgorithm)
        :param digest_size: The (output) digest size to use (Optional[int])
        :return: Whether file name seems like corresponding hash (bool)
        """
        # Get the file name without the extension
        file_name_without_ext = os.path.splitext(file_name)[0]
        expected_length = HashService.get_digest_length_or_none(algorithm)

        file_name_str_len = file_name_without_ext.__len__()

        if file_name_str_len % 1:
            return False

        file_name_bytes = int(file_name_str_len / 2)

        def is_variable_size_valid() -> bool:
            if digest_size is not None:
                return file_name_bytes == digest_size
            return 0 < file_name_bytes <= expected_length

        if HashService.is_digest_length_variable(algorithm):
            has_expected_length = is_variable_size_valid()
        else:
            has_expected_length = file_name_bytes == expected_length

        return has_expected_length and bool(hash_regex.match(file_name_without_ext))

    @staticmethod
    def hash_bytes(data: bytes, hash_function: Callable, digest_size: Optional[int]) -> Optional[str]:
        """
        Hashes and returns the specified binary data depending on the specified hash algorithm and digest size.
        The digest size will be ignored if algorithm is not 'blake2b' or 'blake2s'.
        :param data: The binary data to hash (bytes)
        :param hash_function: The hash function to use (Callable)
        :param digest_size: The digest size to use (Optional<int>)
        :return:
        """
        if digest_size is None:
            hash_function = hash_function()
        else:
            hash_function = hash_function(digest_size=digest_size)
        hash_function.update(data)
        return hash_function.hexdigest()

    @staticmethod
    def hash_file(file_name: str, hash_function: Callable, digest_size: Optional[int]) -> Optional[str]:
        """
        Calculates the hash of a file using the specified algorithm and returns the hex digest
        :param file_name: The file to hash (str)
        :param hash_function: The hash function to use (Callable)
        :param digest_size: The digest size to use (Optional<int>)
        :return: The hash digest (str) or None if an error occurred while reading the file
        """
        file_bytes = FileService.read_file(file_name)
        if file_bytes is None:
            return None
        return HashService.hash_bytes(file_bytes, hash_function, digest_size)

    @staticmethod
    def is_digest_length_variable(algorithm: HashAlgorithm) -> bool:
        """
        Returns whether an algorithm's digest length can be customized.
        :param algorithm: The algorithm to use (HashAlgorithm)
        :return: Whether the specified algorithm allows customizing length (bool)
        """
        result = HashService.get_supported_algorithm_or_none(algorithm)
        if result is None:
            return False
        key = 'variable_length'
        return key in result and result[key] is True


def exit_with_version():
    """
    Print version and maintainer info and exit afterwards.
    """
    print('renash 1.0')
    print('Maintained by lightrain')
    exit(0)


def parse_args() -> Tuple:
    """
    Initialized and parse arguments and return them and the parser
    :return: The arguments parsed and the parser used (Tuple)
    """

    parser = argparse.ArgumentParser(description='Rename files to their hash value')

    # Optional positional
    parser.add_argument('directory', default='.', nargs='?', type=str,
                        help='The directory to process. Use current directory if not set.')

    # Optional
    parser.add_argument('--algorithm', default='sha256', type=str,
                        help=f'Sets the hash algorithm. Available: {HashService.get_supported_hash_algorithms()}')
    parser.add_argument('--dry', action='store_true', help='Dry run. Only prints info about what would be done')
    parser.add_argument('--patterns', default="*.*", type=str,
                        help='A comma separated string of file name glob patterns. Example: "*.jpg,*.mp4"')
    parser.add_argument('--quick', action='store_true', help='Quick run. Skips files that look already properly named')
    parser.add_argument('--size', type=int,
                        help=f'Sets the digest length to use. Works only for algorithms blake2b and blake2s')
    parser.add_argument('--recursive', action='store_true', help='Process directory recursively')
    parser.add_argument('--verbose', action='store_true', help='Print output verbosely')
    parser.add_argument('--version', action='store_true', help='Print version')

    return parser.parse_args(), parser


if __name__ == "__main__":
    args, arg_parser = parse_args()

    if args.version:
        exit_with_version()

    patterns = args.patterns
    pattern_list = args.patterns.split(',')
    print(f"Using pattern{'s' if len(pattern_list) > 1 else ''}: {patterns}")

    target_directory = args.directory

    recursive = args.recursive or False
    absolute_path = os.path.abspath(target_directory)
    print(f"Using virtual base directory {absolute_path}")
    if recursive:
        print(f"Processing recursively")

    hash_algorithm, algorithm_name = HashService.get_hash_algorithm_or_none(args.algorithm)
    if hash_algorithm is None:
        print(f"Unsupported algorithm: {algorithm_name}. Available: {HashService.get_supported_hash_algorithms()}")
        exit(126)

    dry = args.dry
    if dry:
        print("Running in dry mode")

    quick = args.quick
    if quick:
        print("Running in quick mode")

    verbose = args.verbose
    if verbose:
        print("Showing verbose output")

    print(f"Using algorithm {algorithm_name}")

    rename_success = FileService.rename_files(target_directory, pattern_list, hash_algorithm, args.size, recursive,
                                              quick, dry, verbose)
    if rename_success:
        print(StatsService.get_formatted(args.dry))
    else:
        arg_parser.print_help()
