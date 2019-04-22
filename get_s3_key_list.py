#!/usr/bin/env python3
#MIT License
#Copyright (C) 2019 plasticuproject.pm.me

import argparse
import re
import os
import sys
import csv


url = ''
assets = []
sizes_list = []
dates_list = []
etags_list = []
storage_classes_list = []
owner_bool = ''
lastKey = ''
running = True


def run():
    global assets, sizes_list, dates_list, etags_list, storage_classes_list, owner_bool, lastKey, running
    tags = []
    try:
        os.system('wget ' + url + '/?marker=' + lastKey + ' -O 1.html')
        with open('1.html', 'r') as infile:
            for line in infile:
                tags.append(line)
        infile.close()
        ends = (re.findall('(?:<Key>)([\r\s\S]*?)(?:<\/Key>)', tags[1]))
        ##
        sizes = (re.findall('(?:<Size>)([\r\s\S]*?)(?:<\/Size>)', tags[1]))
        dates = (re.findall('(?:<LastModified>)([\r\s\S]*?)(?:<\/LastModified>)', tags[1]))
        etags = (re.findall('(?:<ETag>)([\r\s\S]*?)(?:<\/ETag>)', tags[1]))
        storage_classes = (re.findall('(?:<StorageClass>)([\r\s\S]*?)(?:<\/StorageClass>)', tags[1]))
        owner = (re.findall('(?:<Owner>)([\r\s\S]*?)(?:<\/Owner>)', tags[1]))
        if len(owner) > 0:
            owner_bool = 'Yes'
        else:
            owner_bool = 'No'
        ##
        if len(ends) < 1:
            running = False
        for i in ends:
            assets.append(i)
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
    except:
        print('\nBad URL or connection. Or just broken. Whatever.\n')
        try:
            os.remove('1.html')
        except:
            pass
        sys.exit()


def contents_info():
    with open('contents_info.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Key', 'LastModified', 'ETag', 'Size', 'StorageClass', 'Owner Listed'])
        for i in range(len(assets)):
            writer.writerow(['https://' + url + '/' + assets[i], dates_list[i], etags_list[i], sizes_list[i], storage_classes_list[i], owner_bool])



banner = ('''
    \nInput an S3 Bucket Domain. Since Bucket requests only return 1000 results at
    a time, this script will log the first 1000 Keys, then use the last Key as a
    marker to retrieve more Keys until all of the bucket Keys have been logged.
    It will then print out a file called S3_Keys.txt containing all of the Key
    URLs.\n''')


def main():
    global url
    parser = argparse.ArgumentParser(description=banner)
    parser.add_argument('domain', type=str, metavar='Domain',
                         help='S3 Bucket domain name (example: test.s3.amazonaws.com)')
    args = parser.parse_args()
    url = args.domain
    try:
        while running:
            run()
        with open('S3_Keys.txt', 'w') as outfile:
            for i in assets:
                outfile.write(url + '/' + i + '\n')
            outfile.close()
        contents_info()
        os.remove('1.html')
    except KeyboardInterrupt:
        print('\nSo sorry, me so dum.\n')
        try:
            os.remove('1.html')
        except:
            pass
        sys.exit()
        

if __name__ == '__main__':
    main()
