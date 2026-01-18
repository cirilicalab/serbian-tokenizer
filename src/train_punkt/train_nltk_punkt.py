import argparse
import os
import pickle
from tqdm import tqdm
from nltk.tokenize.punkt import PunktTrainer

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srbtok.srb_tokenizer import normalize_text


def parse_args():
    parser = argparse.ArgumentParser(description='Training corpora for the NLTK Punkt tokenizer.')
    parser.add_argument('-t', '--train', help='Training corpora.', required=True)
    parser.add_argument('-m', '--model', help="Output Punkt model as pickle file.", required=True)
    parser.add_argument('-ad', '--abbreviations-dict', required=False, help="File with list of abbreviations to be manually added to the tokenizer.")
    return parser.parse_args()


def next_batch(file, batch_size):
    lines = []
    while len(lines) < batch_size:
        line = file.readline()
        if not line:
            break
        lines.append(line)
    
    return "".join(lines)


def read_abbreviations_from_file(file_path):
    abbreviations = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.isspace() or line.startswith("#"):
                continue
            abbreviations.add(line.split('\t')[0])
    return abbreviations


def remove_dot_at_end(text):
    end_index = len(text) - 1
    while end_index > 0 and text[end_index] == '.':
        end_index -= 1
    return text[:end_index + 1]


def get_file_size(f):
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)
    return size

if __name__ == "__main__":
    args = parse_args()

    trainer = PunktTrainer()
    batch_size = 100000


    if args.abbreviations_dict:
        print("Adding abbreviations from dictionary: %s" % args.abbreviations_dict)
        read_abbreviations_from_file(args.abbreviations_dict)

    with tqdm(total=1000) as p_bar:
        print = tqdm.write

        print("Using corpora: %s" % args.train)
        with open(args.train, "r", encoding="utf-8") as file:
            train_size = get_file_size(file)

            while file.tell() < train_size:
                print("Reading %d lines" % batch_size)
                text_batch = next_batch(file, batch_size)

                # normalize similar characters to variant that tokenizer will handle
                text_batch = normalize_text(text_batch)

                # run training
                trainer.train(text_batch, finalize=False)

                # prune to reduce mem usage is small
                trainer.freq_threshold()

                # progress bar
                p_bar.n = 1000 * file.tell() // train_size
                p_bar.refresh()
    

    print("Finalize training")
    trainer.finalize_training(verbose=True)
    params = trainer.get_params()


    if args.abbreviations_dict:
        print("Adding abbreviations from dictionary: %s" % args.abbreviations_dict)
        extra_abbreviations = read_abbreviations_from_file(args.abbreviations_dict)
        params.abbrev_types.update(extra_abbreviations)

    print("Saving parameters")
    with open(args.model, "wb") as out_file:
        pickle.dump(params, out_file)
