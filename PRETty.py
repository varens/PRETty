#!/usr/bin/env python

import sys, argparse, re, asyncio

CHUNK_SIZE = 1

def toRE(arg_value):
  return re.compile(arg_value, re.I)

async def probe_printer(printer_ip, args):
  cmd = f'python ./PRET/pret.py {args.debug} -q -i ./commands/{args.command} '\
    f'{printer_ip} {args.shell}'

  print('Command', cmd)

  try:
    process = await asyncio.create_subprocess_shell(
      cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    out, err = await process.communicate()

    print(f'[{cmd!r} exited with {process.returncode}]')

    return out.decode()

  except asyncio.CancelledError:
    raise RuntimeError(f'PRET cancelled on {printer_ip}.') from None

  except Exception as e:
    raise RuntimeError(f'PRET failed on {printer_ip}: {str(e)}') from e

async def process_chunk(chunk, args):
  tasks = [asyncio.create_task(probe_printer(printer_ip, args)) for printer_ip in chunk]

  results = await asyncio.gather(*tasks, return_exception=True)

  for i, result in enumerate(results):
    if isinstance(result, Exception):
      print(f'Error on {chunk[i]}: {str(result)}')
    else:
      print(result)

async def main(args):
  printer_list = args.printers.read().split('\n')[:-1]

  chunks = [printer_list[i:i+CHUNK_SIZE] for i in range(0, len(printer_list),
    CHUNK_SIZE)]
  
  tasks = [asyncio.create_task(process_chunk(chunk, args)) for chunk in chunks]
  
  await asyncio.gather(*tasks)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('printers', nargs='?', type=argparse.FileType('r'),
                      default=sys.stdin, help="A file with a list of printers.\
                      If omitted, the list is read from stdin.")
  parser.add_argument('-c', '--command', type=str,
                      default='pret_pagecount.txt',
                      help='Name of a command-list file to use.')
  parser.add_argument('-m', '--match-condition', type=toRE,
                      default=r'pagecount=\d+',
                      help='A regex indicating an expected probe output.')
  parser.add_argument('-s', '--shell', type=str, default='pjl',
                      help='Printer shell type.', choices=['pjl', 'ps', 'pcl'])
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
    print('Interrupted. Exiting.')
