#!/usr/bin/env python3
################################################################################
# (c) 2023 Copyright, Real-Time Innovations, Inc. (RTI)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
__version__ = "0.1.0"

import os
import sys
import pathlib
import argparse
import subprocess
import argcomplete

_log_verbose = False
_log_quiet = False

def rti_run_command(command):
    log_msg("\n" + os.getcwd() + ">" + " ".join(command))
    subprocess.run(command).check_returncode()

def log_configure(quiet=False, verbose=False):
    global _log_verbose
    global _log_quiet
    _log_verbose = verbose
    _log_quiet = quiet
    if _log_verbose and _log_quiet:
        raise RuntimeError("log both verbose and quiet")

def log_msg(fmt, *args, **kwargs):
    if not _log_verbose and not kwargs.get("force"):
        return
    pfx = kwargs.get("prefix", "-- ")
    fout = kwargs.get("file", sys.stdout)
    line = fmt.format(*list(map(str,args)))
    print("{}{}".format(pfx,line), file=fout)

def log_info(fmt, *args, **kwargs):
    if not _log_verbose and not _log_quiet:
        kwargs["force"] = True
    log_msg(fmt, *args, **kwargs)

def log_warning(fmt, *args, **kwargs):
    if not _log_quiet:
        kwargs["force"] = True
    kwargs["prefix"] = kwargs.get("prefix","-- WARNING: ")
    kwargs["file"] = kwargs.get("file", sys.stderr)
    log_msg(fmt, *args, **kwargs)

def log_error(fmt, *args, **kwargs):
    if not _log_quiet:
        kwargs["force"] = True
    kwargs["prefix"] = kwargs.get("prefix","-- ERROR: ")
    kwargs["file"] = kwargs.get("file", sys.stderr)
    log_msg(fmt, *args, **kwargs)

class RtiCodeGenerator:
    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(
            description="Run rtiddsgen to all files into a specified folder",
            add_help=True)

        gen_opts = parser.add_argument_group(title="general options")

        gen_opts.add_argument("-D", "--directory",
            default=None,
            type=pathlib.Path,
            help="Change current working directory to the specified path.")

        log_opts = gen_opts.add_mutually_exclusive_group()

        log_opts.add_argument("-q","--quiet",
            action="store_true",
            default=False,
            help="Don't produce any additional output to console.")

        log_opts.add_argument("-v","--verbose",
            action="store_true",
            default=False,
            help="Print more information to stdout.")

        gen_opts.add_argument("--version",
            action="version",
            version="%(prog)s " + __version__,
            help="Print script version and exit.")

        opts = parser.add_argument_group(title="required parameters")

        opts.add_argument("-o","--output",
            default=None,
            required=True,
            type=pathlib.Path,
            help="Name of the output directory for the generated files.")

        opt_opts = parser.add_argument_group(title="optional parameters")

        opt_opts.add_argument("-r", "--replace",
            default=False,
            action="store_true",
            help="Overwrite existing files.")

        opt_opts.add_argument("-f", "--files",
            default="*.idl",
            type=str,
            help="Files to process. It may contain wildcards. For example: " +
                "-f \"*.idl\", \"Control*.idl\"")

        opt_opts.add_argument("--skip-files",
            default=None,
            type=str,
            help="Files to skip. It may contain wildcards. For example: " +
                "--skip-files \"*Dcps*.idl\"")

        opt_opts.add_argument("-l", "--language",
            default="C",
            type=str,
            choices=["C", "C++", "Java", "Ada", "C++/CLI", "C++11", "C#",
                     "microC", "microC++", "FACEC++"],
            help="Programming language to generate code for.")

        opt_opts.add_argument("-a", "--architecture",
            default=None,
            type=str,
            help="Generate example files for the specified architecture.")

        opt_opts.add_argument("--dds-types",
            default=False,
            action="store_true",
            help="Add the DDS types defined in dds_dcps.idl")


        opt_opts.add_argument("--additional-options",
            default=None,
            type=str,
            help="Additional rtiddsgen options. For example: --additional_options" +
                "--additional_options=\"-stringSize 1024 -namespace\"")

        return parser

    def __init__(self,
            additional_options=None,
            output=None,
            replace=False,
            basedir=None,
            verbose=False,
            quiet=False,
            language=None,
            architecture=None,
            files=None,
            skip_files=None,
            dds_types=False):

        if dds_types:
            self.dds_dcps_folder = (pathlib.Path(
                os.path.dirname(os.path.abspath(sys.argv[0]))) \
                    / "resource" / "dds_dcps").resolve()
        else:
            self.dds_dcps_folder = None

        if basedir is None:
            self.basedir = pathlib.Path(os.getcwd())
        else:
            self.basedir = pathlib.Path(str(basedir)).resolve()
            os.chdir(str(self.basedir))

        # Create output folder if it doesn't exist
        self.output = pathlib.Path(output).resolve()
        pathlib.Path(self.output).mkdir(parents=True, exist_ok=True)

        self.language = language
        self.architecture = architecture
        self.files_to_process = files
        self.skip_files = skip_files
        self.replace = replace
        self.additional_options = additional_options

        # Configure logging
        log_configure(quiet=quiet, verbose=verbose)
        # Check user input
        self._print_job()

    def _print_job(self):
        log_msg("output folder: {}", self.output)
        log_msg("working directory: {}", self.basedir)
        log_msg("language: {}", self.language)
        log_msg("architecture: {}", self.architecture)
        log_msg("files: {}", self.files_to_process)
        log_msg("skip files: {}", self.skip_files)
        log_msg("replace: {}", self.replace)
        log_msg("use dds_dcps types: {}", True if self.dds_dcps_folder is not None else False)
        log_msg("additional rtiddsgen options: {}", self.additional_options)
        print("\n")

    def process_files(self):
         # Create rtiddsgen call string
        rtiddsgen_options = ["rtiddsgen"]

        if self.additional_options is not None:
            rtiddsgen_options += self.additional_options.split(" ")

        rtiddsgen_options += ["-d",f"{self.output}"]

        if self.replace:
            rtiddsgen_options += ["-replace"]

        rtiddsgen_options += ["-language",f"{self.language}"]

        if self.architecture is not None:
            rtiddsgen_options += ["-example",f"{self.architecture}"]

        if self.dds_dcps_folder is not None:
            rtiddsgen_options += ["-I",f"{self.dds_dcps_folder}"]

        log_msg("Processing files...")

        for e in pathlib.Path(self.basedir).glob(self.files_to_process):
            if self.skip_files is None \
                    or e not in pathlib.Path(self.basedir).glob(self.skip_files):
                rtiddsgen_call = rtiddsgen_options + [str(e)]
                rti_run_command(rtiddsgen_call)

def main():
    parser = RtiCodeGenerator.parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    gen_args = {
        "additional_options": args.additional_options,
        "output": args.output,
        "replace": args.replace,
        "basedir": args.directory,
        "verbose": args.verbose,
        "quiet": args.quiet,
        "language": args.language,
        "architecture": args.architecture,
        "files": args.files,
        "skip_files": args.skip_files,
        "dds_types": args.dds_types,
    }

    # Create output directory if it doesn't exist
    if not os.path.exists(gen_args["output"]):
        os.mkdir(gen_args["output"])

    RtiCodeGenerator(**gen_args).process_files()

main()
