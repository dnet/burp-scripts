#!/usr/bin/env python

from __future__ import print_function, with_statement
from sys import stderr
from os import path

BLOCKSIZE = 4096
SEPARATOR = '\r\n\r\n'

def process(files):
    for file_name in files:
        output_name = file_name + '.nohead'
        if path.exists(output_name):
            print('{0} already exists, skipping {1}'.format(output_name,
                file_name), file=stderr)
            continue
        found_header = False
        with file(file_name, 'rb') as http_resp:
            with file(output_name, 'wb') as output:
                while True:
                    input_block = http_resp.read(BLOCKSIZE)
                    if not input_block:
                        break
                    if found_header:
                        output.write(input_block)
                    else:
                        idx = input_block.find(SEPARATOR)
                        if idx >= 0:
                            output.write(input_block[idx + len(SEPARATOR):])
                            found_header = True


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        print('Usage: {0} file1 [file2] ...'.format(argv[0]), file=stderr)
    else:
        process(argv[1:])
