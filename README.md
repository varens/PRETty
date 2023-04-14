# PRETty
Please refer to the parent reposity and [PRET](https://github.com/RUB-NDS/PRET) for background information on what this is.

This fork is a rewrite of the parent with a focus on a subjectively more convenient CLI interface, no automatic scanning, and no interfactive prompts. The reasoning behind the effort is to integrate enumeration of potentially vulnerable printers into larger automated processes. Hence the assumtion that target IP addresses/ranges are known in advance and no user input is required throughout the tool's execution.

## Installation

1. install the prerequisites
  - get `imagemagick` and `ghostscript` from package manager of choice
  - run `pip install -r requirements.txt`
2. get PRETty:
  - `git clone --recurse-submodules https://github.com/varens/PRETty`

## PRET command lists

PRETty comes with pre-made command list files for PRET located in `PRETty/commands/`; however, others can be added and specified in the call to `PRETty.py`.

## Usage
```
usage: PRETty.py [-h] [-c COMMAND] [-m MATCH_CONDITION] [-s {pjl,ps,pcl}] [-d] [printers]

positional arguments:
  printers              A file with a list of printers. If omitted, the list is read from stdin.

options:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Name of a command-list file to use.
  -m MATCH_CONDITION, --match-condition MATCH_CONDITION
                        A regex indicating an expected probe output.
  -s {pjl,ps,pcl}, --shell {pjl,ps,pcl}
                        Printer shell type.
  -d, --debug
```

PRETty.py takes a list of printer IPs from STDIN or a file and outputs addresses of printers to which PRET was able to connect and `--command` output matched the `--match-condition`. The defaults for command and match condition are `pagecount` and `r'pagecount=\d+'`.

For example:

```
python PRETty.py path/to/input/file --command pret_pagecount.txt --match-condition 'pagecount=\d+' > vuln_printers
```

```
cat list_of_printers | python PRETty.py > vuln_printers
```
