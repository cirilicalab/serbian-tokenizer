#!/bin/bash

train_corpora=../../data/train/train.txt
dst=../srbtok/serbian_punkt_nltk.pickle

python train_nltk_punkt.py --train ${train_corpora} --model ${dst}
