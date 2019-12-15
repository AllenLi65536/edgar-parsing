#!/bin/bash
# bash recompress.sh 07
tar -xvf edgar-10k-mda/form10k$1.tar.gz
tar -zcvf edgar-10k-mda/form10k$1.tar.gz -C edgar-10k-mda form10k$1
rm -r edgar-10k-mda/form10k$1

