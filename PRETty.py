#!/usr/bin/env python

import asyncio, re, argparse, sys, os

def toRE(arg_value):
  return re.compile(arg_value, re.I)

async def probe_printer(ip, args):
  os.chdir(os.path.dirname(__file__))
  command = f'python ./PRET/pret.py {args.debug} -q -i '\
    f'./commands/{args.command} {ip} {args.shell}'
  
  try:
    process = await asyncio.create_subprocess_shell(command,
      stdout=asyncio.subprocess.PIPE)

    output, error = await process.communicate()

    if not args.match_condition.search(output.decode()):
      return None
    return ip

  except asyncio.CancelledError:
    raise RuntimeError(f'PRET cancelled on {ip}.') from None

  except Exception as e:
    raise RuntimeError(f'PRET failed on {ip}: {str(e)}') from e

async def process_chunk(chunk, args):
  tasks = [asyncio.create_task(probe_printer(ip, args)) for ip in chunk]

  results = await asyncio.gather(*tasks, return_exceptions=True)

  for i, result in enumerate(results):
    if isinstance(result, Exception):
      print(f'Error processing {chunk[i]}: {str(result)}')
    else:
      if result: print(result)

async def main(args):
  chunk_size = 5

  ips = args.printers.read().split('\n')[:-1]

  chunks = [ips[i:i+chunk_size] for i in range(0, len(ips), chunk_size)]

  tasks = [asyncio.create_task(process_chunk(chunk, args)) for chunk in chunks]

  await asyncio.gather(*tasks)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('printers', nargs='?', type=argparse.FileType('r'),
                      default=sys.stdin, help="A file with a list of printers.\
                      If omitted, the list is read from stdin.")
  parser.add_argument('-c', '--command', type=str,
                      default='pret_pagecount.txt',
                      help='File in ./commands with a list of pret commands to run on the printer.')
  parser.add_argument('-m', '--match-condition', type=toRE,
                      default=r'pagecount=\d+',
                      help='A regex indicating an expected probe output.')
  parser.add_argument('-s', '--shell', type=str, default='pjl',
                      help='Printer shell type. Defaults to pjl',
                      choices=['pjl', 'ps', 'pcl'])
  parser.add_argument('-d', '--debug', action='store_const', const='-d',
                      default='')

  args = parser.parse_args()

  try:
    asyncio.run(main(args))

  except KeyboardInterrupt:
    for task in asyncio.all_tasks():
      task.cancel()

  finally:
    asyncio.run(asyncio.sleep(0.250))
