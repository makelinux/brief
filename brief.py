#!/usr/bin/env python3

import re
import os
import sys
import fnmatch
import argparse

args = rest_args = None

remove = "|".join([
    r'\s*//+\s*',       # //
    r'\s*/\*+\s*',      # /*
    r'^\s*\*\s*\s+',    #  *
    r'\s*\*/',          #  */
    r'^\s+',
    r'\s*\n$',
    'SPDX.*',
    r'\(C\).*|Copyright.*',
    'All Rights Reserved.*',
    'Written.*|Author.*|Rewritten.*',
])


def file_brief(file_path):
    res = ''
    n = 0
    _, fn = os.path.split(file_path)
    comment = False
    with open(file_path, 'r') as fo:
        while l := fo.readline():
            if m := re.search(r'MODULE_DESCRIPTION\("([^"]*)"\)', l):
                res = m.group(1)
                break
            n += 1
            if not comment and re.match(r'\s*/\*', l):
                comment = True
            comment2 = re.match(r'\s*//', l)
            t = re.sub(remove, '', l, flags=re.IGNORECASE)
            # remove filename
            t = re.sub('\S*' + re.escape(fn) + r'\b:?\s*-*\s*', '', t)
            t = re.sub(r'\s+', ' ', t)
            if t and len(res) < 80 and (comment or comment2):
                res += (' ' if len(res) else '') + t
            if args.debug:
                print(len(res), res, len(t), t, comment, l, file=sys.stderr)
            if comment and re.match(r'.*\*/', l):
                comment = False
    return file_path + ': ' + res


def brief(input='.',):
    if os.path.isfile(input):
        print(file_brief(input))
    ext = set('.h .c .S .hh hpp .cpp'.split())
    for path, dirs, files, _ in os.fwalk(input):
        path = re.sub(r'^\.\/', '', path)
        if args.debug:
            print(path, file=sys.stderr)
        for f in sorted(files):
            _, e = os.path.splitext(f)
            if e in ext:
                if fnmatch.fnmatch(f, '*.mod.c'):
                    continue
                print(file_brief(os.path.join(path, f)))
        if not args.recursive:
            break


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--recursive', action='store_true',
                    help='scan subdirectories recursively')
    ap.add_argument('-d', '--debug', action='store_true',
                    help='trace debug information')
    args, rest_args = ap.parse_known_args()
    if args.debug:
        print(args, file=sys.stderr)
        print(rest_args, file=sys.stderr)
    if not rest_args:
        brief()
    else:
        for i in rest_args:
            brief(i)
