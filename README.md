# PRETty
"PRinter Exploitation Toolkit" LAN automation tool
 (It's just a python wrapper for PRET... actually it's really just a for loop)

This is a minor rewrite of the original tool with a focus on non-interactive execution.
No third-party modules, besides pysnmp and colorama required by PRET, are imported by the tool.

PRETty is useful when a large number of printers are present on a network. Instead of scanning, logging, and manually running PRET againt each individual printer, PRETty will automatically discover and run choosen PRET payloads against all printers on the target network.

Additionally, PRETty can be used to automate command/payload delivery to any given list of printers (See the "Lists" section)

# GUIDE:

## Installation

1. install the prerequisites
  - `sudo apt -y install imagemagick ghostscript arp-scan tshark`
  - pysnmp and colorama are required by PRET which may installed with pip or your OS package manager
2. set up [PRET](https://github.com/RUB-NDS/PRET) by making pret.py executable and available in your PATH, for example:
  - `git clone https://github.com/RUB-NDS/PRET`
  - `chmod +x PRET/pret.py`
  - `PATH=$PATH:$(pwd)/PRET`
3. set up PRETty:
  - `git clone https://github.com/varens/PRETty`
  - `chmod +x PRETty/PRETty.py`

## Lists
* PRETty automatically scans the LAN for HP/Brother/Kyocera printers and creates an IP list for itself
	* However, you can place custom IP lists in `PRETty/IP/`
* PRETty comes with pre-made command list files for PRET located in `PRETty/commands/`
	* However, you can place additional command list files in `PRETty/commands/`
	
## Usage
* Run PRETty with `./PRETty.py` and follow the prompts :D
* For more advanced users, run `./PRETty.py -h`
	* `./PRETty.py --cli` enables CLI mode. (No user input required)
	* The default `./PRETty.py --cli` will run `./commands/pret_pagecount.txt` on every printer in `./IP/Printer_list` or a file supplied by `-l`. Output from the given command will be matched against a case-insensitive regex specified by `-m` and appended to a file specified by `-o`. Most arguments assume opinionated defaults, for example a simple `--cli` run equals the following:
  `PRETty.py --cli -c pret_pagecount.txt -m 'pagecount=\d+' -l ./IP/Printer_list -o ./IP/MMDDYY.list

## Disclaimers
### The standard internet fun disclaimer applies. Don't commit crimes, be responsible. 
### I am in no way responsible for anything and everything you do with PRETty.
--
VGhlIGNvZGUgaXMgZ3Jvc3MsIG5vb2IteSBhbmQgaW5lZmZpY2llbnQuIEJ1dCBpdCB3b3JrcywgYW5kIGl0J3MgbXkgZmlyc3QgcmVhbCBwcm9qZWN0LiBTbyBJJ20gcHJvdWQgOkQKClRoaXMgaXMgYSBmb3IgbG9vcC4gVGhlIG9ubHkgcGFydCBvZiB0aGlzIGNvZGUgdGhhdCBtYXR0ZXJzIGlzIGF0IHRoZSBib3R0b20uCgpodHRwczovL3R3aXR0ZXIuY29tL0J1c2VzQ2FuRmx5L3N0YXR1cy8xMDgwOTQ5OTkzMTgyMjk0MDE3
--
