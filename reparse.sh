#!/bin/bash
# bash -x reparse.sh 07
# $1 = 07 # 2007

# Decompress files from archive
tar -C edgar-10k-mda -xvf edgar-10k-mda/form10k$1.tar.gz 

# Extract item 1 and item 7 from files
python3 edgar-10k-mda/edgar.py extract mda --10k-dir=edgar-10k-mda/form10k$1 --mda-dir=edgar-10k-mda/form10k$1

# Parse files and get frequency dictionary
python3 Parsing.py edgar-10k-mda/form10k$1_item1
python3 Parsing.py edgar-10k-mda/form10k$1_item7

# Remove original decompressed files
rm -r edgar-10k-mda/form10k$1
rm -r edgar-10k-mda/form10k$1_item1
rm -r edgar-10k-mda/form10k$1_item7

# Get similarity matrix
#python3 GetSimiliarity.py edgar-10k-mda/form10k$1_item1_dict
#python3 GetSimiliarity.py edgar-10k-mda/form10k$1_item7_dict

# Get clusters
#python3 GetClusters.py edgar-10k-mda/form10k$1_item1_dict
#python3 GetClusters.py edgar-10k-mda/form10k$1_item7_dict

# Recompress
#tar -xvf edgar-10k-mda/form10k$1.tar.gz
#tar -zcvf edgar-10k-mda/form10k$1.tar.gz -C edgar-10k-mda form10k$1
#rm -r edgar-10k-mda/form10k$1
