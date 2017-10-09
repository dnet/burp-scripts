#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from collections import defaultdict
from lxml import etree
import re

LOC_XPATH = etree.XPath('location/text()')
LOC_RE = re.compile(r'^/([^ ]+) \[(.*) parameter]$')

def process_file(input_file, output_file, encoding='utf-8'):
    issues = etree.parse(input_file).getroot()
    pages = defaultdict(set)
    for issue in issues:
        params = LOC_RE.match(''.join(LOC_XPATH(issue)))
        page, param_name = params.groups()
        if not param_name:
            param_name = '(empty)'
        elif 'arbitrarily supplied' in param_name:
            param_name = '(arbitrary)'
        pages[page].add(param_name)
    for page, parameters in sorted(pages.iteritems()):
        output_file.write('{0}\t{1}\n'.format(
            page, ', '.join(sorted(parameters))).encode(encoding))

if __name__ == '__main__':
    from sys import argv, stderr, stdout
    if len(argv) < 2:
        print("Usage: {0} <file.xml> [output.csv]".format(argv[0]), file=stderr)
        raise SystemExit(1)
    if len(argv) < 3:
        process_file(argv[1], stdout)
    else:
        with file(argv[3], 'w') as f:
            process_file(argv[1], f)
