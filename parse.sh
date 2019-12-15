#!/bin/bash
# bash parse.sh 2007 07

# $1 = 2007
# $2 = 07 # short year

# Download index files
python3 edgar-10k-mda/edgar.py download index --year-start=$1 --year-end=$1 --index-dir=edgar-10k-mda/index$2  --index-10k-path=edgar-10k-mda/index.10k$2.csv

# Download 10k files
python3 edgar-10k-mda/edgar.py download 10k --index-10k-path=edgar-10k-mda/index.10k$2.csv --10k-dir=edgar-10k-mda/form10k$2

# Extract item 1 and item 7 from files
python3 edgar-10k-mda/edgar.py extract mda --10k-dir=edgar-10k-mda/form10k$2 --mda-dir=edgar-10k-mda/form10k$2

# Parse files and get frequency dictionary
python3 Parsing.py edgar-10k-mda/form10k$2_item1
python3 Parsing.py edgar-10k-mda/form10k$2_item7
#python3 Parsing.py /home/li/EDGAR/MyParsing/edgar-10k-mda/form10k$2_item1
#python3 Parsing.py /home/li/EDGAR/MyParsing/edgar-10k-mda/form10k$2_item7

# Compress files
tar -zcvf edgar-10k-mda/form10k$2.tar.gz -C edgar-10k-mda form10k$2

# Remove original downloaded files
#rm -r edgar-10k-mda/form10k$2
