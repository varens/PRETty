#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from subprocess import run, PIPE, STDOUT
from time import sleep

alt_text = ' automation tool'

def main_text():
  print("              \"PRinter Exploitation Toolkit\" LAN"+alt_text+"             ")
def main_art():
  print("PRETTY")
  main_text()
  print("-------------------------------------------------------------------------------")
def interactive_steps():
  print("Step 1: Generate IP list")
  print("Step 2: Select IP list")
  print("Step 3: Select PRET command input file")
  print("Step 4: Select shell type")
  print("Step 5: Observe all laws and ethical/moral codes :D")
  print("Step 6: >:)\n")

parser = argparse.ArgumentParser()
parser.add_argument('--cli', dest='cli', action='store_true',
                    help='Enable CLI mode (No user input)')
parser.add_argument('-r', '--ip-range', type=str, default='--localnet',
                    help='IP range to scan')
parser.add_argument('-c', '--commands-list', type=str, default='pret_pagecount.txt',
                    help='Name of command list file to use')
parser.add_argument('-s', '--shell-type', type=str, default='ps',
                    help='Printer shell type for PRET')
parser.add_argument('-a', '--arp-scan', action='store_true',
                    help='Perform an arp scan')
parser.add_argument('-l', '--printer-list', default='./IP/Printer_list',
                    help='A file with a list of printers to probe')

args = parser.parse_args()

sleep_time=1.5
def PrinterLogSort():
  os.system('tshark -r ./IP/scan.pcap > ./IP/pcap.txt 2>/dev/null')
  os.system('cat ./IP/pcap.txt | grep -iE "Hewlett|Brother|Kyocera|Laserjet" > ./IP/raw_list 2>/dev/null')
  os.system('awk \'{print $8}\' ./IP/raw_list > ./IP/Printer_list')
  sleep(0.5)
  print('Successfully processed raw data')
  os.system('rm -rf ./IP/scan.pcap && rm -rf ./IP/pcap.txt && rm -rf ./IP/raw_list 2>/dev/null')
  sleep(sleep_time)
  print('Cleaned raw data')
  sleep(sleep_time)
  print('\nLocated '+ str(sum(1 for line in open ('./IP/Printer_list'))) +' printers, storing as ./IP/Printer_list\n')

def PRETty_Interactive():
  gen_new= str(input("Generate new IP list? [y/N] "))
  if gen_new == 'y':

    set_ip_range = input("Set IP range for scanning? [y/N] ")
    if set_ip_range == 'y':
      ip_range = str(input("IP range: [ex. 192.168.0.0/16] "))
    else:
      ip_range = '--localnet'

    print("ARP scanning LAN for devices...")
    sleep(1.5)
    os.system('sudo arp-scan -g '+ip_range+' -W ./IP/scan.pcap')
    print('Successfully collected IP\'s')

    PrinterLogSort()

  list_answer = str(input("Use default IP list? [Y/n] "))
  if list_answer == 'n':
    print('An example IP list can be found at ./IP/example')
    print('Available IP lists: ')
    os.system('ls ./IP/')
    print('\n')
    list = './IP/' + str(input("Which list? ./IP/"))
    print('\nLoaded '+ str(sum(1 for line in open (list))) +' IP\'s\n')
  else:
    print('Using "./IP/Printer_list" as IP range')
    list = './IP/Printer_list'
    print('\nLoaded '+ str(sum(1 for line in open ('./IP/Printer_list'))) +' IP\'s\n')

  commands_list = str(input("Use default ./commands/pret_pagecount.txt command file? [Y/n] "))
  if commands_list == 'n':
    print('Example command lists: (./commands)')
    os.system('ls ./commands/')
    print('\n')
    commands_list = './commands/' + str(input("Which command list? "+'./commands/'))
    print('Commands: ')
    os.system('cat '+commands_list)
    print('\n')
  else:
    print('Using "./commands/pret_pagecount.txt" as PRET commands')
    commands_list = './commands/pret_pagecount.txt'
    print('Commands: ')
    os.system('cat ./commands/pret_pagecount.txt')
    print('\n')

  shell_type = input("Shell Type: [ps, pjl, pcl] ")

  debug = input('Enable PRET debug mode? [y/N] ')
  if debug == 'y':
    debug_enabled = '-d'
  else:
    debug_enabled = ''
  print('')

  with open(list) as inf:
    lines = [line.strip() for line in inf]

  i=0
  while i < len(lines):
    os.system('../pret.py '+debug_enabled+' -i '+commands_list+' -q '+lines[i]+' '+ shell_type)
    i+=1

def PRETty_cli():
  # avoid breaking current functionality
  if args.arp_scan:
    os.system('sudo arp-scan -g '+args.ip_range+' -W ./IP/scan.pcap')
    PrinterLogSort()
    sleep(1)
    list = './IP/Printer_list'
    with open(list) as inf:
      lines = [line.strip() for line in inf]
    i=0
    while i < len(lines):
      os.system('../pret.py -i ./commands/'+args.commands_list+' -q '+lines[i]+' '+ args.shell_type)
      i+=1
  else:
    with open(args.printer_list) as inf:
      for printer_ip in inf:
        ProbePrinter(printer_ip.rstrip(), f'./commands/{args.commands_list}')

def ProbePrinter(ip, commands_file, shell_type='pjl'):
  print('open assigned to %r' % open)
  cmd = f'../pret.py -i {commands_file} -q {ip} {shell_type}'
  with run(cmd, stdout=PIPE, stderr=STDOUT, shell=True) as pret_proc:
    print(pret_proc.stdout.read())

if args.cli:
  main_art()
  sleep_time=0.5
  PRETty_cli()
else:
  alt_text = ' automation tool'
  main_art()
  interactive_steps()
  sleep_time=1.5
  PRETty_Interactive()

