#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
tokenize="python3 ${SCRIPT_DIR}/../../tools/nltk_tokenize.py --sent-tokenizer PunktTokenizer(russian) --word-tokenizer TreebankWordTokenizer"

in_file=$1
out_file=$2

echo tokenize ${in_file} 
cat ${in_file} | $tokenize > ${out_file}
