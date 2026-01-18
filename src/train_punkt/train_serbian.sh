#!/bin/bash

train_corpora=../../data/train/train.txt
abbreviations_dict=../../data/train/abbreviations_dict.txt

dst=../srbtok/serbian_punkt_nltk.pickle

python3 train_nltk_punkt.py --train ${train_corpora} --abbreviations-dict ${abbreviations_dict}  --model ${dst}
