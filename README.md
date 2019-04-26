# GetS3Keys

Since AWS S3 Bucket requests only return 1000 results at a time, **get_s3_key_list.py** <br />
will log the first 1000 Keys, then use the last Key as a marker to retrieve more <br />
Keys until all of the bucket Keys have been logged. It will then output a file <br />
called **"URL"_Keys.txt** containing all of the Key URLs. It will also create **"URL"_Info.csv** <br />
containing various information about the Key files. <br />


## Requirements

Linux OS <br />
Python 3.6+ <br />
wget <br />


## Usage
Run **get_s3_key_list.py** to download bucket content URLs.
```
usage: get_s3_key_list.py [-h] Domain

Input an S3 Bucket Domain. Since Bucket requests only return 1000 results at a
time, this script will log the first 1000 Keys, then use the last Key as a
marker to retrieve more Keys until all of the bucket Keys have been logged. It
will then print out a file called "URL"_Keys.txt containing all of the Key
URLs., and "URL"_Info.csv containing information about each Key file.

positional arguments:
  Domain      S3 Bucket domain name (example: test.s3.amazonaws.com)

optional arguments:
  -h, --help  show this help message and exit

```

