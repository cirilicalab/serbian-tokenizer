#!/bin/bash

set -xe

src_dir=~/Downloads/politika/text/2025/
raw_dir=raw
expected_dir=expected
count=100

# rm -rf ${raw_dir}
# rm -rf ${expected_dir}

# if [ -d "$raw_dir" ]; then
#   echo "Exiting $raw_dir already exists."
# fi

# mkdir -p ${raw_dir}
# mkdir -p ${expected_dir}
# find ${src_dir} -type f | shuf -n ${count} | xargs -I {} cp {} raw/

tokenizer="../../../src/srbtok/punktrus_toktok.sh"
# find ${raw_dir} -type f | sed "s/${raw_dir}\///g" | xargs -I {} ${tokenizer} ${raw_dir}/{} ${expected_dir}/{}

find expected/ -type f | xargs cat | sed 's/ /\n/g' | sort | uniq > words.txt
