import sys
import argparse

from .utils import tokenize_stream_sent_per_line, tokenize_stream
from .srb_tokenizer import SrbTokenizer



def parse_args():
    parser = argparse.ArgumentParser(description='This tool tokenizes Serbian Cyrillic text to sentences and words.')
    parser.add_argument('-i', '--in-text', help='Input text file that you want to tokenize. If not specified stdin will be used.', required=False)
    parser.add_argument('-o', '--out-text', help="Output text with tokenized text. If not specified stdout will be used.", required=False)
    parser.add_argument('-spl', '--sent-per-line', action='store_true', help='Write one sentence per line in output file. If not specified original formatting will be preserved.')
    return parser.parse_args()




if __name__ == "__main__":
    '''Implementation of tokenization tool. This is the module __main__ method.'''
    args = parse_args()

    tokenizer = SrbTokenizer()

    istream = sys.stdin
    if args.in_text:
        istream = open(args.in_text, 'r', encoding='utf-8')

    ostream = sys.stdout
    if args.out_text:
        ostream = open(args.out_text, 'w', encoding='utf-8')
    
    if args.sent_per_line:
        out_text = tokenize_stream_sent_per_line(istream, tokenizer)
    else:
        out_text = tokenize_stream(istream, tokenizer)
    ostream.write(out_text)
