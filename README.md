[![python](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/download/releases/3.0/)

### Description
Data differ, compare and update data from loaders.

### Installation

Install from Github

    pip3 install git+https://github.com/delatars/data_diff
    
### Usage

```bash
$ data_diff -h
usage: entrypoint.py [-h] [--mode {auto,manual}] [--loaders]
                     loader_from_uri loader_to_uri

Data differ

positional arguments:
  loader_from_uri       loader with actual data.
  loader_to_uri         loader where data will be updated.

optional arguments:
  -h, --help            show this help message and exit
  --mode {auto,manual}, -m {auto,manual}
                        Set differ mode: manual|auto (default: manual)
  --loaders, -l         Show available loaders

```

##### available loaders

```bash
$ data_diff -l
File Loaders:
   .xls            - file://file.xls or ~/file.xls
   .xlsx           - file://file.xlsx or ~/file.xlsx
Web Loaders:
   docs.google.com - https://docs.google.com/spreadsheet/ccc?key=0Bm...FE&hl
```

### Docker

##### Build
```bash
$ git clone https://github.com/delatars/data_diff
$ cd data_diff
$ docker build -t data_diff .
```

##### Run
```bash
$ docker run --rm data_diff -h
```