"""
  File    : ZMAKE.py
  Purpose : Build Z-Image Workflows from source templates and configuration files.
  Author  : Martin Rizzo | <martinrizzo@gmail.com>
  Date    : Sep 18, 2026
  Repo    : https://github.com/martin-rizzo/ZImageTotalFun
  License : Unlicense
 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                             Z-Image Total Fun!!!
        Creative and wild visual style workflows for Z-Image Turbo model.
 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
"""
from __future__ import annotations
import os
import sys
import argparse
from pathlib import Path

# default directory where to look for source files
DEFAULT_SOURCE_DIR = "src"


# ANSI escape codes for colored terminal output
RED      = '\033[91m'
DKRED    = '\033[31m'
YELLOW   = '\033[93m'
DKYELLOW = '\033[33m'
GREEN    = '\033[92m'
CYAN     = '\033[96m'
DKGRAY   = '\033[90m'
RESET    = '\033[0m'

#----------------------------- ERROR MESSAGES ------------------------------#

def disable_colors():
    global RED, DKRED, YELLOW, DKYELLOW, GREEN, CYAN, DKGRAY, RESET
    RED, DKRED, YELLOW, DKYELLOW, GREEN, CYAN, DKGRAY, RESET = "", "", "", "", "", "", "", ""


def info(message: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an informational message to the error stream.
    """
    print(f"{' '*padding}{CYAN}\u24d8 {message}{RESET}", file=file)


def warning(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a warning message to the standard error stream.
    """
    print(f"{' '*padding}{CYAN}[{YELLOW}WARNING{CYAN}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        info(info_message, padding=padding, file=file)


def error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an error message to the standard error stream.
    """
    print(f"{' '*padding}{DKRED}[{RED}ERROR!{DKRED}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        info(info_message, padding=padding, file=file)


def fatal_error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a fatal error message to the standard error stream and exits with status code 1.
    """
    error(message, *info_messages, padding=padding, file=file)
    sys.exit(1)


#--------------------------------- HELPERS ---------------------------------#

class ZMakeParser:
    """
    Parser for ZMAKE instruction files (zmakefile).

    Handles parsing of lines from ZMAKE instruction files, identifying
    instructions, parameters, and content blocks, and executing them sequentially.
    Maintains local and global variable dictionaries.
    """

    def __init__(self):
        """Initialize the parser."""
        self.local_vars  : dict[str, str] = { }
        self.global_vars : dict[str, str] = { }


    @staticmethod
    def is_zmake_file(file_path: str) -> bool:
        """
        Determines if a given file is a ZMAKE instruction file.

        Args:
            file_path: The path to the file to be checked.

        Returns:
            `True` if the file starts with '@zmakefile', `False` otherwise.
        """
        try:
            with open(file_path, 'r') as f:
                first_chars = f.read(20)
                return first_chars.upper().startswith("@ZMAKEFILE")
        except Exception as e:
            return False


    def execute_instruction(self,
                            instruction: str,
                            params     : list[str],
                            content    : list[str],
                            /,*,
                            base_dir: Path,
                            overwrite_files: bool = False,
                            recursive_count: int  = 0,
                            ) -> None:
        """
        Execute a single instruction with its parameters and content.

        Args:
            instruction: The name of the instruction to execute.
            params     : A list of parameters associated with the instruction.
            content    : A list of content lines associated with the instruction.
            base_dir   : The base directory for resolving relative paths.
            overwrite_files: Whether to overwrite existing output files.
            recursive_count: The current depth of recursive execution.
        """
        # DUMMY FUNCTION
        print("==========================")
        print(f"INSTRUCTION: {instruction}")
        print(f"PARAMS: {params}")
        print(f"CONTENT: {content}")


    def execute_lines(self,
                      lines: list[str] | str,
                      /,*,
                      base_dir: Path,
                      overwrite_files: bool = False,
                      recursive_count: int  = 0,
                      ) -> int:
        """
        Parse and execute a list or string of lines containing ZMAKE instructions.

        Args:
            lines: A string or list of strings containing ZMAKE instructions.
            base_dir: The base directory for resolving relative paths.
            overwrite_files: Whether to overwrite existing output files.
            recursive_count: The current depth of recursive execution.

        Returns:
            The total number of instructions executed.
        """
        instr_count     : int       = 0
        pending_instr   : str       = ""
        pending_params  : list[str] = [ ]
        pending_content : list[str] = [ ]
        lines_to_execute: list[str]

        if isinstance(lines, str):
            lines_to_execute = lines.strip().splitlines()
        elif isinstance(lines, list):
            lines_to_execute = lines
        else:
            raise ValueError("Invalid lines argument")

        # add sentinel element (EOF instruction)
        # to force processing of last instruction
        if lines_to_execute and not lines_to_execute[-1].upper().startswith(">::EOF"):
            lines_to_execute = lines_to_execute + [">::EOF"]

        for line in lines_to_execute:

            # end parsing if the EOF instruction was found
            if pending_instr == "EOF":
                break

            # ignore comments
            if line.startswith(">::/"):
                continue

            # when a new instruction marker is detected,
            # the previous pending instruction must be processed
            if line.startswith(">::"):
                if pending_instr:
                    self.execute_instruction(pending_instr, pending_params, pending_content,
                                             base_dir        = base_dir,
                                             overwrite_files = overwrite_files,
                                             recursive_count = recursive_count)
                    instr_count += 1

                # store the detected instruction as pending
                instr, _, params = line[3:].strip().partition(" ")
                instr  = instr.strip()
                params = params.strip()
                pending_instr   = instr.upper()
                pending_params  = params.split() if len(params) > 1 else []
                pending_content = []

            # the line does not contain any marker,
            # it is text that must be added to the pending content
            else:
                pending_content.append(line)

        return instr_count


    def execute_file(self,
                     filepath: Path,
                     /,*,
                     overwrite_files: bool = False,
                     recursive_count: int  = 0
                     ) -> int:
        """
        Read a ZMAKE instruction file and execute its contents.

        Args:
            filepath: The path to the ZMAKE instruction file (zmakefile).
            overwrite_files: Whether to overwrite existing output files.
            recursive_count: The current depth of recursive execution.

        Returns:
            The number of instructions executed, or 0 on failure.
        """
        try:
            with open(filepath, 'r') as f:
                lines = f.read()
            base_dir = filepath.parent
            return self.execute_lines(lines,
                                      base_dir = base_dir,
                                      overwrite_files = overwrite_files,
                                      recursive_count = recursive_count)
        except Exception as e:
            error(f"Failed to process {filepath}: {e}")
            return 0



#===========================================================================#
#////////////////////////////////// MAIN ///////////////////////////////////#
#===========================================================================#


def main(args=None, parent_script=None):
    """
    Main entry point for the script.
    Args:
        args          (optional): List of arguments to parse. Default is None, which will use the command line arguments.
        parent_script (optional): The name of the calling script if any. Used for customizing help output.
    """    
    prog = None
    if parent_script:
        prog = parent_script + " " + os.path.basename(__file__).split('.')[0]

    # set up argument parser for the script
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Build Z-Image Workflows from source templates and configuration files.",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument('--no-color'       , action='store_true', help="Disable colored output.")
    parser.add_argument('-s','--source-dir', type=str,            help="The source dir containing templates and config files (default: /src)")
    parser.add_argument('-w','--overwrite' , action='store_true', help="Overwrite existing output file if exists.")


    args = parser.parse_args(args=args)

    # if the user requested to disable colors, call disable_colors()
    if args.no_color:
        disable_colors()

    # get source directory and convert it to absolute path
    source_dir = args.source_dir or DEFAULT_SOURCE_DIR
    source_dir = os.path.join(os.getcwd(), source_dir)
    source_dir = os.path.realpath(source_dir)

    # gather .txt files that are valid ZMAKE instruction files
    all_zmakefile_paths: list[Path] = []
    for filename in os.listdir(source_dir):
        if filename.endswith(".txt") and ZMakeParser.is_zmake_file(os.path.join(source_dir, filename)):
            all_zmakefile_paths.append( Path(source_dir) / filename )

    # display errors if no zmakefiles were found
    if len(all_zmakefile_paths) == 0:
        fatal_error("No valid text configuration files found in the source directory.")

    # process the found zmakefiles one by one
    for zmakefile_path in all_zmakefile_paths:
        print(f' Building workflows from "{os.path.basename(zmakefile_path)}"')
        zmakeparser = ZMakeParser()
        zmakeparser.execute_file(zmakefile_path, overwrite_files = args.overwrite)
        print()



if __name__ == "__main__":
    main()
