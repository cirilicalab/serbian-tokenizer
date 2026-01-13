#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
tokenize="python ${SCRIPT_DIR}/../../tools/nltk_tokenize.py --sent-tokenizer PunktTokenizer(russian) --word-tokenizer SrbRegexpTokenizer --sent-per-line"

in_file=$1
out_file=$2

echo tokenize ${in_file} 
cat ${in_file} | $tokenize > ${out_file}
