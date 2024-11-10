#!/usr/bin/python3

from os import path
from sys import argv
from pathlib import Path
from time import time
import re


def show_help():
    print(
    """Usage: ./LineCounter.py <path to dir> <suffixes> <ignore_patterns (optional)>
-----------------------------------------------
    Path to dir    : Path to start counting from. (Recursive!)
    Suffixes       : List of file suffixes. Files ending like given suffixes will be counted (whitelist)
        Example -> "c,py,css,js"
    Ignore Patterns: Folders including any of the given patterns are ignored when counting.
        Does not apply to files! Example -> "vscode,test,node_modules"
    """)


def check_for_larger_file(file_list: list, nf: str, lc: int):
    """Checks input values and adds them to the list if the lc is greater than one in the list

    lc [int]: line_count
    nf [str]: file name of new file
    file_list [list]: List of biggest current files
    """
    if lc > file_list[0][1]:
        file_list[4] = file_list[3]
        file_list[3] = file_list[2]
        file_list[2] = file_list[1]
        file_list[1] = file_list[0]
        file_list[0] = (nf, lc)
        return

    if lc > file_list[1][1]:
        file_list[4] = file_list[3]
        file_list[3] = file_list[2]
        file_list[2] = file_list[1]
        file_list[1] = (nf, lc)
        return

    if lc > file_list[2][1]:
        file_list[4] = file_list[3]
        file_list[3] = file_list[2]
        file_list[2] = (nf, lc)
        return

    if lc > file_list[3][1]:
        file_list[4] = file_list[3]
        file_list[3] = (nf, lc)
        return

    if lc > file_list[4][1]:
        file_list[4] = (nf, lc)


def ls(root_path: Path, to_ignore: list) -> [Path, list, list]: # type: ignore
    if not root_path.is_dir():
        raise FileNotFoundError(f"Provided Path not found: '{path}'")

    files = []
    dirs = []
    for entry in root_path.iterdir():
        ignore = False
        for ign in to_ignore:
            if ign in entry.name:
                ignore = True
                break
        if ignore:
            continue

        if entry.is_dir():
            dirs.append(entry)
            for r, d, f in ls(entry, to_ignore):
                yield r, d, f

        if entry.is_file():
            files.append(entry)

    yield root_path, dirs, files


if __name__ == "__main__":
    largest_files = [("XXX", 0)]*5
    line_count = 0
    code_count = 0
    file_count = 0
    dir_count = 0
    total_words = 0
    code_blocks = []

    if len(argv) != 3 and len(argv) != 4:
        print(f"\033[31mNot enough arguments! Expected 2 got {len(argv)-1}! -> {argv}\033[0m")
        show_help()
        exit(-1)

    if not path.isdir(argv[1]):
        print("\033[31mPath could not be opened or is not a directory!\033[0m")
        exit(-1)

    starttime = time()
    suffixes = {suf[0]: [0, 0] for suf in zip(argv[2].replace(" ", "").split(","))}

    to_ignore = []
    if len(argv) == 4:
        to_ignore = argv[3].replace(" ", "").split(",")

    for root, dirs, files in ls(Path(argv[1]), to_ignore):
        print(f"Searching {root}...{' ':20}", end="\r")
        dir_count += len(dirs)
        for fp in files:
            file_suffix = fp.suffix.lower()[1:]
            if file_suffix not in suffixes.keys():
                continue

            file_count += 1
            with open(fp, "r", encoding="UTF-8") as fd:
                lc = 0
                code_block = 0
                for line in fd.readlines():
                    line_count += 1
                    suffixes[file_suffix][0] += 1
                    if len(line.strip()) > 0:
                        total_words += len(list(filter(lambda w: len(w) > 1, re.split(r"[ \.\(\)\{\}\[\]=]", line))))
                        lc += 1
                        code_block += 1
                    elif code_block > 0:
                        code_blocks += [code_block]
                        code_block = 0
                code_count += lc
                suffixes[file_suffix][1] += lc
                check_for_larger_file(largest_files, fp.name, lc)

    name_len = len(max(largest_files, key=lambda file: len(file[0]))[0])
    lf_str = f"\n    {largest_files[0][0]:.<{name_len}} = {largest_files[0][1]}"
    lf_str += f"\n    {largest_files[1][0]:.<{name_len}} = {largest_files[1][1]}"
    lf_str += f"\n    {largest_files[2][0]:.<{name_len}} = {largest_files[2][1]}"
    lf_str += f"\n    {largest_files[3][0]:.<{name_len}} = {largest_files[3][1]}"
    lf_str += f"\n    {largest_files[4][0]:.<{name_len}} = {largest_files[4][1]}"

    suffix_str = "\033[33mSplit by Suffix:\033[0m"
    for suffix in sorted(suffixes, key=lambda x: suffixes[x][0], reverse=True):
        suffix_str += f"\n    {suffix:4}: {suffixes[suffix][0]:7} ({suffixes[suffix][1]})"

    timestr = f"Searched {dir_count} folders in {time()-starttime:.2f}s"

    if file_count > 0:
        print(
f"""\033[33m---   Line Counter Results   ---\033[0m
All Lines : {line_count}
Code Lines: {code_count}

File-Count: {file_count}
Avg. Lines: {code_count/file_count:.1f} (Code Only)
Avg. Block: {sum(code_blocks)/len(code_blocks):.2f} lines

\033[33mFive Largest Files:\033[0m{lf_str}

{suffix_str}

\033[33mTotal "Words":\033[0m {total_words}
{timestr}"""
)
