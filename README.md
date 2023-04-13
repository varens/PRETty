# PRETty (rewritten)
Please refer to the parent reposity and [PRET](https://github.com/RUB-NDS/PRET) for background information on what this is.

This fork is a complete rewrite of the parent with a focus on a subjectively more convenient CLI interface, no automatic scanning, and no interfactive prompts. The reasoning behind the effort is to integrate enumeration of potentially vulnerable printers into larger automated processes. Hence the assumtion that target IP addresses/ranges are known in advance and no user input is required throughout the tool's execution.

## GUIDE:

### Installation

1. install the prerequisites
  - get `imagemagick` and `ghostscript` from package manager of choice
  - run `pip install -r requirements.txt`
2. get PRETty:
  - `git clone --recurse-submodules https://github.com/varens/PRETty`

## Lists

* PRETty comes with pre-made command list files for PRET located in `PRETty/commands/`
	* However, you can place additional command list files in `PRETty/commands/`
	
## Usage
* Run PRETty with `./PRETty.py` and follow the prompts :D
* For more advanced users, run `./PRETty.py -h`
	* `./PRETty.py --cli` enables CLI mode. (No user input required)
	* The default `./PRETty.py --cli` will run `./commands/pret_pagecount.txt` on every printer in `./IP/Printer_list` or a file supplied by `-l`. Output from the given command will be matched against a case-insensitive regex specified by `-m` and appended to a file specified by `-o`. Most arguments assume opinionated defaults, for example a simple `--cli` run equals the following:
  `PRETty.py --cli -c pret_pagecount.txt -m 'pagecount=\d+' -l ./IP/Printer_list -o ./IP/MMDDYY.list`

