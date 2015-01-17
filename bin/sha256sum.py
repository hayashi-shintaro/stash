'''
sha256sum - Get md5 hash of a file. Supports pipes.

usage: sha256sum.py [-h] [-c] file

positional arguments:
  file         File to get sha256sum or file contailing a list of hashes and files

optional arguments:
  -h, --help   show this help message and exit
  -c, --check  Check a file with sha256 values and files for a match. format:
               sha256_hash filename
               sha256_hash filename
               etc.
'''
import argparse
from Crypto.Hash import SHA256
import re
import sys
import os

def get_sha256(fileobj):
    h = SHA256.new()
    chunk_size = 8192
    while True:
        chunk = fileobj.read(chunk_size)
        if len(chunk) == 0:
            break
        h.update(chunk)
    return h.hexdigest()
    
def check_list(filename):
    with open(filename,'r') as f:
        for line in f:
            match = re.match(r'(\w+)[ \t]+(.+)',line)
            try:
                with open(match.group(2),'rb') as f1:
                    if match.group(1) == get_sha256(f1):
                        print match.group(2)+': Pass'
                    else:
                        print match.group(2)+': Fail'
            except:
                break
    
        
ap = argparse.ArgumentParser()
ap.add_argument('-c','--check',action='store_true',default=False,
                help='''Check a file with sha256 values and files for a match. format: sha256_hash filename''')
ap.add_argument('file',action='store',nargs='?',help='File to get sha256sum or file contailing a list of hashes and files')
args = ap.parse_args(sys.argv[1:])

if args.check:
    if args.file:
        check_list(args.file)
    else:
        pipe = sys.stdin.read().rstrip().replace('\n',' ').split(' ')
        for line in pipe:
            if os.path.isfile(line):
                check_list(line)
else:
    if args.file:
        with open(args.file,'rb') as f:
            print get_sha256(f)
    else:
        pipe = sys.stdin.read().rstrip().replace('\n',' ').split(' ')
        for line in pipe:
            if os.path.isfile(line):
                with open(line,'rb') as f:
                    print '%s %s'% (get_sha256(f),line)
