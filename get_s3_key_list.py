#!/usr/bin/env python3
#MIT License
#Copyright (C) 2019 plasticuproject.pm.me


import subprocess
import argparse
import re
import os
import sys
import csv


url = ''
lastKey = ''
oldKey = 'init'
running = True

banner = ('''
    \nInput an S3 Bucket Domain. Since Bucket requests only return 1000 results at
    a time, this script will log the first 1000 Keys, then use the last Key as a
    marker to retrieve more Keys until all of the bucket Keys have been logged.
    It will then print out a file called "URL"_Keys.txt containing all of the Key
    URLs., and "URL"_Info.csv containing information about each Key file.\n''')


def write_keys(assets):

    new_url = url.replace('/', '-')
    with open(new_url + '_Keys.txt', 'a') as outfile:
        for i in assets:
            outfile.write(url + '/' + i + '\n')
        outfile.close()
    os.remove('1.html')


def contents_info(assets, dates_list, etags_list, sizes_list, storage_classes_list, owner_bool):

    new_url = url.replace('/', '-')
    with open(new_url + '_Info.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(assets)):
            writer.writerow([url + '/' + assets[i], dates_list[i], etags_list[i], sizes_list[i], storage_classes_list[i], owner_bool[0]])


def clean_up():

    try:
        os.remove('1.html')
        quit()
    except:
        quit()


def run():
    
    global running, lastKey, oldKey
    assets = []
    sizes_list = []
    dates_list = []
    etags_list = []
    storage_classes_list = []
    owner_bool = ['No']
    tags = []

    try:
        if oldKey == lastKey:
            clean_up()

        subprocess.run(['wget', url + '/?marker=' + lastKey, '-O', '1.html'])
        oldKey = lastKey
        with open('1.html', 'r') as infile:
            for line in infile:
                tags.append(line)
        infile.close()
        ends = (re.findall('(?:<Key>)([\r\s\S]*?)(?:<\/Key>)', tags[1]))
        sizes = (re.findall('(?:<Size>)([\r\s\S]*?)(?:<\/Size>)', tags[1]))
        dates = (re.findall('(?:<LastModified>)([\r\s\S]*?)(?:<\/LastModified>)', tags[1]))
        etags = (re.findall('(?:<ETag>)([\r\s\S]*?)(?:<\/ETag>)', tags[1]))
        storage_classes = (re.findall('(?:<StorageClass>)([\r\s\S]*?)(?:<\/StorageClass>)', tags[1]))
        owner = (re.findall('(?:<Owner>)([\r\s\S]*?)(?:<\/Owner>)', tags[1]))
        if len(owner) > 0:
            for i in owner:
                owner_bool = []
                owner_bool.append('Yes')
        if len(ends) < 1:
            running = False
        for i in ends:
            clean = i.replace('&amp;', '&')
            clean = clean.replace('&quot;', '"')
            clean = clean.replace('&apos;', "'")
            clean = clean.replace(' ', "+")
            assets.append(clean)
        for i in sizes:
            sizes_list.append(i)
        for i in dates:
            dates_list.append(i)
        for i in etags:
            clean = i.replace('&quot;', '')
            etags_list.append(clean)
        for i in storage_classes:
            storage_classes_list.append(i)
        lastKey = assets[-1]
        write_keys(assets)
        contents_info(assets, dates_list, etags_list, sizes_list, storage_classes_list, owner_bool)
    except:
        clean_up()
        

def main():

    global url
    parser = argparse.ArgumentParser(description=banner)
    parser.add_argument('domain', type=str, metavar='Domain',
                         help='S3 Bucket domain name (example: test.s3.amazonaws.com)')
    args = parser.parse_args()
    url = args.domain

    try:
        new_url = url.replace('/', '-')
        with open(new_url + '_Info.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Key', 'LastModified', 'ETag', 'Size', 'StorageClass', 'Owner Listed'])
        while True:
            run()
    except KeyboardInterrupt:
        clean_up()
        

if __name__ == '__main__':
    main()
