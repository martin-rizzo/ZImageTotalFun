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
import json
import argparse
from pathlib import Path
from typing import overload, NoReturn

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


def message(msg: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a plain progress/status message to the specified stream.
    """
    print(f"{' ' * padding}{msg}", file=file)


def info(message: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an informational message to the error stream.
    """
    print(f"{' '*padding}{CYAN}\u24d8 {message}{RESET}", file=file)


def warning(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a warning message to the standard error stream.
    """
    print(f"{' '*padding}{CYAN}[{YELLOW}WARNING{CYAN}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        if info_message:
            info(info_message, padding=padding, file=file)


def error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an error message to the standard error stream.
    """
    print(f"{' '*padding}{DKRED}[{RED}ERROR!{DKRED}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        if info_message:
            info(info_message, padding=padding, file=file)


def fatal_error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> NoReturn:
    """Displays a fatal error message to the standard error stream and exits with status code 1.
    """
    error(message, *info_messages, padding=padding, file=file)
    sys.exit(1)


#----------------------------- RELATIVE PATHS ------------------------------#

_reference_dir: Path = Path(__file__).resolve().parent


def set_reference_dir(dirpath: Path | str) -> None:
    """
    Set the reference directory used for computing relative paths.

    This function updates the reference dir, which is used  by the `rel()`
    function to compute relative paths. All error messages that contain file
    paths will be displayed relative to this directory, making them easier
    to understand.

    Args:
        dirpath: The directory path to set as the reference. Can be a `Path`
                 object or a string.
    """
    global _reference_dir
    _reference_dir = Path(dirpath).resolve()


def rel(path: Path | str) -> str:
    """
    Return a relative path to the reference directory.

    This function attempts to compute the relative path from the reference
    directory (set via `set_reference_dir()`). If the path is not under the
    reference directory, the absolute path is returned as a fallback.

    This is primarily used in error messages to display file paths in a
    human-readable, relative form.

    Args:
        path: The path to convert. Can be a `Path` object or a string.

    Returns:
        A string representing the path. If the path is under the reference
        directory, returns a relative path prefixed with './'. Otherwise,
        returns the absolute path.
    """
    target_path = Path(path).resolve()
    try:
        return './' + str(target_path.relative_to(_reference_dir))
    except ValueError:
        return str(target_path)


#----------------------------- CLASS VarSolver -----------------------------#

class VarSolver:
    """
    A class for solving variables in template strings.

    This class maintains two dictionaries: one for unsolved variables
    (variables that need to be resolved) and one for solved variables
    (variables that have already been resolved). It provides methods
    to add variables, retrieve their values, and solve template strings
    by replacing variable placeholders with their resolved values.

    Attributes:
        unsolved_vars (dict[str, str]): Dictionary of unresolved variables.
        solved_vars   (dict[str, str]): Dictionary of resolved variables.
        _resolving   (set[str])       : Set of variables currently being resolved
                                        to detect circular dependencies.
    """

    def __init__(self):
        """
        Initialize the VarSolver instance.
        """
        self.unsolved_vars: dict[str, str] = {}
        self.solved_vars  : dict[str, str] = {}
        self._resolving   : set[str]       = set()


    def add_vars(self, new_vars: dict[str, str]) -> None:
        """
        Add new variables to the solver.

        Args:
            new_vars: A dictionary of variable names and their values
                      to be added to the solver.
        """
        # when new variables are added, ALL variables become 'unresolved'
        # since it is unknown whether any resolved variables indirectly depend
        # on these newly added/modified variables
        self.solved_vars = {}

        # add the new variables
        self.unsolved_vars.update(new_vars)


    def get_value(self, var_name: str) -> str | None:
        """
        Retrieve the value of a variable, resolving it if necessary.

        This method first checks if the variable has already been resolved.
        If not, it attempts to resolve the variable by replacing all
        variable placeholders within its value with their resolved values.
        Circular dependencies are detected and raise a ValueError.

        Args:
            var_name: The name of the variable to retrieve.

        Returns:
            The resolved value of the variable, or None if the variable
            does not exist.

        Raises:
            ValueError: If a circular dependency is detected during resolution.
        """
        # variables that have already been resolved are accessed directly
        if var_name in self.solved_vars:
            return self.solved_vars[var_name]

        # if the variable is still unresolved,
        # it is resolved by replacing all variables referenced within it
        elif var_name in self.unsolved_vars:

            # check for circular dependencies
            if var_name in self._resolving:
                raise ValueError(f"Circular dependency detected in variable '{var_name}'")

            unsolved_value = self.unsolved_vars[var_name]
            try:
                self._resolving.add(var_name)
                solved_value = self.solve(unsolved_value)
            finally:
                self._resolving.remove(var_name)

            # mark variable as resolved and return the resulting value
            self.solved_vars[var_name] = solved_value
            return solved_value

        # if the variable does not exist at all, return None
        else:
            return None


    @overload
    def solve(self, target: str) -> str: ...

    @overload
    def solve(self, target: list) -> list: ...

    @overload
    def solve(self, target: dict) -> dict: ...


    def solve(self, target: str | list | dict) -> str | list | dict:
            """
            Recursively resolve variables in a string, list, or dictionary.

            This method replaces all variable placeholders in the format
            {#var_name} with their resolved values. The resolution is
            performed recursively, so nested lists and dictionaries are
            also processed.

            Args:
                target: The string, list, or dictionary to resolve.

            Returns:
                A new object with all variable placeholders replaced by
                their resolved values.
            """
            if isinstance(target, str):
                return self._solve_string(target) if "{#" in target else target

            elif isinstance(target, list):
                return [self.solve(item) for item in target]

            elif isinstance(target, dict):
                return {key: self.solve(item) for key, item in target.items()}

            return target


    def _solve_string(self, string: str) -> str:
        """
        Solve a template string by replacing variable placeholders with their values.

        Args:
            string: The template string containing variable placeholders
                    in the format {#var_name}.

        Returns:
            The resolved string with all variable placeholders replaced
            by their corresponding values.
        """
        result: list[str] = []
        segments: list[str] = string.split("{#")

        result.append(segments.pop(0))
        for segment in segments:
            var_value : str | None = None
            remainder : str        = ""

            if "}" in segment:
                var_name, remainder = segment.split("}", 1)
                var_value = self.get_value(var_name)

            # If the variable's value could not be obtained, either because the
            # segment does not contain "}" or because the variable is undefined
            # then keep the original text segment
            if var_value is None:
                result.append("{#" + segment)
                continue

            result.append( var_value )
            result.append( remainder )

        return "".join(result)


#---------------------------- CLASS ZMakeParser ----------------------------#

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
    def is_zmake_file(file_path: Path | str) -> bool:
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


    def set_var(self, var_name: str, var_value: str | list[str], /, persistent: bool) -> None:
        """
        Set a variable value, either globally or locally.

        Args:
            var_name:   The name of the variable.
                        Leading '#' characters are stripped.
            var_value:  The value to assign.
                        If a list, values are joined with newlines.
            persistent: If True, the variable is stored globally and persists
                        for the entire duration of the script execution.
                        If False, the variable is stored locally and is only
                        valid until the next MAKE instruction is encountered.
        """
        value = "\n".join(var_value) if isinstance(var_value, list) else var_value
        if persistent: self.global_vars[var_name.lstrip('#')] = value
        else:          self.local_vars [var_name.lstrip('#')] = value


    def load_var(self, var_name: str, filepaths: list[Path], /, persistent: bool) -> None:
        """
        Load the contents of one or more text files into a variable.

        Args:
            var_name:   The name of the variable to store the contents in.
            filepaths:  A list of Path objects pointing to the text files
                        to load.
            persistent: If True, the variable is stored globally and persists
                        for the entire duration of the script execution.
                        If False, the variable is stored locally and is only
                        valid until the next MAKE instruction is encountered.

        Raises:
            FileNotFoundError: If any of the specified files do not exist.
            ValueError: If any file appears to be binary or cannot be decoded as UTF-8.
        """
        # verify that all files exist and are not binary files
        for filepath in filepaths:
            if not filepath.is_file():
                raise FileNotFoundError(f"File '{rel(filepath)}' does not exist.")
            with filepath.open('rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:
                    raise ValueError(f"File '{rel(filepath)}' appears to be a binary file, expected a text file.")

        # if validation passes, read the contents of all files and concatenate them
        contents: list[str] = []
        for filepath in filepaths:
            try:
                file_content = filepath.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                raise ValueError(f"File {filepath} cannot be decoded as UTF-8 text.")
            contents.append(file_content)

        self.set_var(var_name, contents, persistent)


    def make(self,
             dest_path: Path,
             /,*,
             template_path  : Path,
             var_solver     : VarSolver | None = None,
             overwrite_files: bool             = False
             ):
        """Builds a file replacing the variables in the template file."""

        if not overwrite_files and dest_path.is_file():
            raise FileExistsError(f"Destination file '{rel(dest_path)}' already exists. Use --overwrite to overwrite.")

        if not template_path.is_file():
            raise FileNotFoundError(f"Template file '{rel(template_path)}' does not exist.")

        if var_solver is None:
            var_solver = VarSolver()
            var_solver.add_vars( self.global_vars )
            var_solver.add_vars( self.local_vars  )

        file_type = template_path.suffix.lower().lstrip(".")
        with open(template_path, 'r') as f:
            template = f.read()

        if file_type == "txt":
            with open(dest_path, 'w') as f:
                f.write( var_solver.solve(template) )

        elif file_type == "json":
            raw_data      = json.loads(template)
            resolved_data = var_solver.solve(raw_data)
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump( resolved_data, f, indent=4, ensure_ascii=False )
        else:
            raise ValueError(f"Unsupported template file type '{file_type}'. Only 'txt' and 'json' are supported.")


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
        instruction = instruction.strip().upper()

        if instruction == "EOF":
            pass

        elif instruction == "SET!":
            var_name = params[0]
            self.set_var( var_name, content, persistent=True )

        elif instruction == "SET":
            var_name = params[0]
            self.set_var( var_name, content, persistent=False )

        elif instruction == "LOAD!":
            var_name  : str        = params[0]
            filepaths : list[Path] = [base_dir / c_line.strip() for c_line in content if c_line.strip()]
            self.load_var(var_name, filepaths, persistent=True )

        elif instruction == "LOAD":
            var_name  : str        = params[0]
            filepaths : list[Path] = [base_dir / c_line.strip() for c_line in content if c_line.strip()]
            self.load_var(var_name, filepaths, persistent=False )

        elif instruction == "MAKE":
            var_solver = VarSolver()
            var_solver.add_vars( self.global_vars )
            var_solver.add_vars( self.local_vars  )
            for line in content:
                line = var_solver.solve(line)
                dest_file, _, template_file = line.partition(":")
                if dest_file and template_file:
                    self.make(base_dir / dest_file.strip(),
                              template_path   = base_dir / template_file.strip(),
                              var_solver      = var_solver,
                              overwrite_files = overwrite_files)


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


    def execute_zmakefile(self,
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
            error(f"Failed to process '{rel(filepath)}':\n  {e}")
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
    parser.add_argument('zmakefiles'      , type=str, nargs='*', default=[], help="One or more zmakefile files (or directories containing zmakefiles) to be processed.")
    parser.add_argument('-w','--overwrite', action='store_true', help="Overwrite existing output files.")
    parser.add_argument('-n','--no-color' , action='store_true', help="Disable colored output.")
    args = parser.parse_args(args=args)

    # if the user requested to disable colors, call disable_colors()
    if args.no_color:
        disable_colors()

    working_dir = Path.cwd()
    set_reference_dir(working_dir)

    # collect all zmakefiles that were supplied directly as arguments,
    # or are found inside directories that were supplied as arguments.
    all_zmakefile_paths: list[Path] = []
    for file_or_dir in args.zmakefiles:
        file_or_dir_path : Path = working_dir / file_or_dir

        if file_or_dir_path.is_file() and ZMakeParser.is_zmake_file(file_or_dir_path):
            all_zmakefile_paths.append(file_or_dir_path)

        elif file_or_dir_path.is_dir():
            for child_path in file_or_dir_path.iterdir():
                if child_path.is_file() and ZMakeParser.is_zmake_file(child_path):
                    all_zmakefile_paths.append(child_path)


    # display errors if no zmakefiles were provided
    if len(all_zmakefile_paths) == 0:
        fatal_error("No valid zmakefile was provided")

    # process the provided zmakefiles
    for zmakefile_path in all_zmakefile_paths:
        message(f' Building workflows from "{os.path.basename(zmakefile_path)}"')
        zmakeparser = ZMakeParser()
        zmakeparser.set_var("#PWD", str(working_dir), persistent=True)
        zmakeparser.execute_zmakefile(zmakefile_path, overwrite_files = args.overwrite)



if __name__ == "__main__":
    main()
