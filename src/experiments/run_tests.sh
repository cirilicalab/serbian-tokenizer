#!/bin/bash

set -xe



# location of all test datasets
test_dir=../../data/test


run_one_test() {
    dataset_name=$1
    tokenizer_name=$2

    dataset_dir=${test_dir}/${dataset_name}
    tokenizer=tokenizers/${tokenizer_name}.sh

    out_dir=out/${dataset_name}/${tokenizer_name}
    mkdir -p ${out_dir}
    mkdir -p ${out_dir}/tokenized

    # run tokenization
    cat ${dataset_dir}/file_list.txt | xargs -I {} ${tokenizer} ${dataset_dir}/raw/{} ${out_dir}/tokenized/{}

    # compute result
    python ../tools/score.py --expected-dir ${dataset_dir}/expected --actual-dir ${out_dir}/tokenized --per-file-results ${out_dir}/per_file_results.tsv > ${out_dir}/result.tsv
}


# run_one_test politika punktrus_whitespace
# run_one_test politika punktrus_treebank
# run_one_test politika punktrus_srbregex
# run_one_test politika punktsrb_srbregex

cut -f1,5,3 out/politika/punktrus_whitespace/result.tsv | sed 's/\t/ | /g' > results.md
cut -f1,5,3 out/politika/punktrus_whitespace/result.tsv | sed 's/[a-zA-Z]/-/g' | sed 's/\t/ | /g' >> results.md
cut -f2,6,4 out/politika/punktrus_whitespace/result.tsv | sed 's/\t/ | /g' >> results.md
cut -f2,6,4 out/politika/punktrus_treebank/result.tsv | sed 's/\t/ | /g' >> results.md
cut -f2,6,4 out/politika/punktrus_srbregex/result.tsv | sed 's/\t/ | /g' >> results.md
cut -f2,6,4 out/politika/punktsrb_srbregex/result.tsv | sed 's/\t/ | /g' >> results.md
