# run-rtiddsgen

`run-rtiddsgen` is a command-line utility that will run `rtiddsgen` in a bunch
of files. These files can be selected from a pattern that includes wildcards.
It can also skip files to avoid generate code for them. And, of course, it
allows you to use all `rtiddsgen` options.

## Installation

Clone the repository and install it with pip:

```sh
git clone https://github.com/angelrti/run-rtiddsgen.git
pip3 install run-rtiddsgen
```

## Requirements

This does require to have a valid and executable rtiddsgen installed in your
computer. You may get that executable by installing RTI Connext DDS.

## Usage

```
usage: __init__.py [-h] [-D DIRECTORY] [-q | -v] [--version] -o OUTPUT [-r] [-f FILES] [--skip-files SKIP_FILES] [-l {C,C++,Java,Ada,C++/CLI,C++11,C#,microC,microC++,FACEC++}] [-a ARCHITECTURE] [--dds-types]
                   [--additional-options ADDITIONAL_OPTIONS]

Run rtiddsgen to all files into a specified folder

options:
  -h, --help            show this help message and exit

general options:
  -D DIRECTORY, --directory DIRECTORY
                        Change current working directory to the specified path.
  -q, --quiet           Don't produce any additional output to console.
  -v, --verbose         Print more information to stdout.
  --version             Print script version and exit.

required parameters:
  -o OUTPUT, --output OUTPUT
                        Name of the output directory for the generated files.

optional parameters:
  -r, --replace         Overwrite existing files.
  -f FILES, --files FILES
                        Files to process. It may contain wildcards. For example: -f "*.idl", "Control*.idl"
  --skip-files SKIP_FILES
                        Files to skip. It may contain wildcards. For example: --skip-files "*Dcps*.idl"
  -l {C,C++,Java,Ada,C++/CLI,C++11,C#,microC,microC++,FACEC++}, --language {C,C++,Java,Ada,C++/CLI,C++11,C#,microC,microC++,FACEC++}
                        Programming language to generate code for.
  -a ARCHITECTURE, --architecture ARCHITECTURE
                        Generate example files for the specified architecture.
  --dds-types           Add the DDS types defined in dds_dcps.idl
  --additional-options ADDITIONAL_OPTIONS
                        Additional rtiddsgen options. For example: --additional_options--additional_options="-stringSize 1024 -namespace"
```

## Examples

- Run `rtiddsgen` for all the idle files in the `datamodel/idl/` folder that
  start by `Sensor`. The output folder for the generated files is
  `delete_generated_files/`. It will skip files that contains the text `Dcps`,
  and increase the rtiddsgen verbosity to be `error`.

  ```sh
  run-rtiddsgen -v -D datamodel/idl -o delete_generated_files -f "Sensor*.idl" --additional-options="-verbosity 1" --skip-files "*Dcps*.idl"
  ```
