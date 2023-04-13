#!/usr/bin/env python

import os, sys, argparse, re
from subprocess import run, PIPE, STDOUT

def toRE(arg_value):
  return re.compile(arg_value, re.I)


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
    with open(args.printer_list) as inf, open(args.output_file, 'w') as outf:
      for printer_ip in inf:
        probe_output = ProbePrinter(printer_ip.rstrip(), f'./commands/{args.commands_list}', args.shell_type)
        print(probe_output)
        if ProbePassed(probe_output, args.match_condition):
          outf.write(printer_ip)

def ProbePrinter(ip, commands_file, shell_type):
  cmd = ['pret.py', '-i', commands_file, '-q', ip, shell_type]
  pret_done = run(cmd, stdout=PIPE, stderr=STDOUT)
  return pret_done.stdout.decode()

def ProbePassed(output, re_condition):
  if 'established' not in output:
    return False
  return bool(re_condition.search(output))

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

def main(printers, command, match_condition, shell):
  if printers == sys.stdin:
    pass
  else:
    pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('printers', nargs='?', type=argparse.FileType('r'),
                      default=sys.stdin, help="A file with a list of printers.\
                      If omitted, the list is read from stdin.")
  parser.add_argument('-c', '--command', type=str,
                      default='pret_pagecount.txt',
                      help='Name of a command-list file to use.')
  parser.add_argument('-m', '--match-condition', type=toRE, default=r'pagecount=\d+',
                      help='A regex indicating an expected probe output.')
  parser.add_argument('-s', '--shell', type=str, default='pjl',
                      help='Printer shell type.', choices=['pjl', 'ps', 'pcl'])

  args = parser.parse_args()
  main(**vars(args))