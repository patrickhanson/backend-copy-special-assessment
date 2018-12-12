#!/usr/bin/env python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import re
import os
import shutil
import subprocess
import argparse


def collect_paths(directory):
    file_directory = os.listdir(directory)
    match_file = [os.path.abspath(file)
                  for file in file_directory
                  if re.search(r'__\w+__', file)]
    return match_file


def copy_files(list_of_paths, todir):
    if os.path.exists(todir):
        for file in list_of_paths:
            shutil.copy(file, todir)
            print """Added file: {file}
            to new directory: {todir}""".format(file=file, todir=todir)
    elif not os.path.exists(todir):
        os.makedirs(todir)
        for file in list_of_paths:
            shutil.copy(file, todir)
            print """Added file: {file}
            to new directory: {todir}""".format(file=file, todir=todir)


def zip_files(zipfile, list_of_paths):
    zip_list = ['zip', '-j', zipfile]
    zip_list.extend(list_of_paths)
    print 'Command I am going to do:'
    print ' '.join(zip_list)
    """With Piero's assistance"""
    try:
        subprocess.check_output(zip_list)
    except subprocess.CalledProcessError as e:
        print e.output
        exit(e.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('from_dir', help='dir files are currently in')
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    args = parser.parse_args()

    collected_paths = collect_paths(args.from_dir)
    if not collected_paths:
        print 'no files match'
    elif collected_paths and args.todir:
        copy_files(collected_paths, args.todir)
    elif args.tozip:
        zip_files(args.tozip, collected_paths)
    else:
        print 'i am bamboozled'


if __name__ == "__main__":
    main()
