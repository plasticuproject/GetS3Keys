# GetS3Keys

Since AWS S3 Bucket requests only return 1000 results at a time, **get_s3_key_list.py** <br />
will log the first 1000 Keys, then use the last Key as a marker to retrieve more <br />
Keys until all of the bucket Keys have been logged. It will then print out a file <br />
called **S3_Keys.txt** containing all of the Key URLs. It will also create **contents_info.csv** <br />
containing the bucket keys with file size and last modified dates. <br />


## Requirements

Linux OS <br />
Python 3.6+ <br />
wget <br />


## Usage
Run **get_s3_key_list.py** to download bucket content URLs.
```
usage: get_s3_key_list.py [-h] Domain

positional arguments:
  Domain      S3 Bucket domain name (example: test.s3.amazonaws.com)

optional arguments:
  -h, --help  show this help message and exit
```

