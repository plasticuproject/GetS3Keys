#!/usr/bin/env python3
#MIT License
#Copyright (C) 2019 plasticuproject.pm.me

from csv import reader
import argparse


banner =("""
    Feed this program your CSV File to return the combined size of
    all the files in the S3 Bucket.""")


def add(inFile):

    sizes = []
    with open(inFile, 'r') as file:
        csv_reader = reader(file)
        line_count = 0
        for row in csv_reader:
            try:
                int(row[3])
                sizes.append(row[3])
                line_count += 1
                print('Row: ' + str(line_count))
            except:
                line_count += 1
                print('FUCKED UP LINE ITEM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                pass
    amount = 0
    for i in sizes:
        i = int(i)
        amount += i
    print(str(amount) + ' Bytes')
    print(str(amount // 1024) + ' KB')
    print(str(amount // 1024 // 1024) + ' MB')
    print(str(amount // 1024 // 1024 // 1024) + ' GB')


def main():

    parser = argparse.ArgumentParser(description=banner)
    parser.add_argument('csv', type=str, metavar='CSV File',
                         help='S3 Bucket CSV File (example: test.s3.amazonaws.com_Info.csv)')
    args = parser.parse_args()
    inFile = args.csv

    try:
        add(inFile)
    except Exception as e:
        print(e)
        quit()


if __name__ == '__main__':
    main()

