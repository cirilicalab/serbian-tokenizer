import os
import sys
import argparse

from nltk.tokenize import TreebankWordTokenizer, WhitespaceTokenizer, PunktTokenizer, ToktokTokenizer

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srbtok.srb_tokenizer import SrbRegexpWordTokenizer, create_serbian_punkt_tokenizer
from srbtok.cascade_tokenizer import CascadeTokenizer
from srbtok.utils import tokenize_stream_sent_per_line, tokenize_stream

#
#  - екс - Yу ово је очигледна грешка у транслитерацији са латинице на ћирилицу
#  - \xa0 : alt space, can confuse sentence segmentation algorithm and also word segmentation algorithm. This can be solved by normalization of the strings as we are not changing the number of characters.
#

# Црта
#  - раздвајамо праве две речи повезена цртом - Ана Живковић - Марковић, пензијско - инвалидски фонд, плеј - оф
#  - не раздвајамо наставак за падеж: МУП-а, 91-их година, 
#  - раздвајамо јединице: 91 - годишњи
#

def parse_args():
    parser = argparse.ArgumentParser(description='Runs NLTK tokenizer on input text. If no input is specified stdin will be used as input. Output written to stdout.')
    parser.add_argument('-i', '--in-text', help='Input text file.', required=False)
    parser.add_argument('-t', '--tokenized-text', help="Output tokenized text file.", required=False)
    parser.add_argument('-st', '--sent-tokenizer', default="none", help='NLTK sentence tokenization algorithm')
    parser.add_argument('-wt', '--word-tokenizer', required=True, help='NLTK word tokenization algorithm')
    parser.add_argument('-spl', '--sent-per-line', action='store_true', help='Write one sentence per line in output file')
    return parser.parse_args()


WORD_SEP = ' '


class DummyTokenizer:
    def span_tokenize(self, text):
        return [(0, len(text))]


def create_sent_tokenizer(spec_str):
    if spec_str == "PunktTokenizer(english)":
        return PunktTokenizer("english")
    
    elif spec_str=="PunktTokenizer(russian)":
        return PunktTokenizer("russian")
    
    elif spec_str=="PunktTokenizer(serbian)":
        return create_serbian_punkt_tokenizer()
    
    elif spec_str == "None":
        return DummyTokenizer()


def create_word_tokenizer(spec_str):
    if spec_str == "TreebankWordTokenizer":
        return TreebankWordTokenizer()
    
    elif spec_str == "WhitespaceTokenizer":
        return WhitespaceTokenizer()
    
    elif spec_str == "ToktokTokenizer":
        return ToktokTokenizer()
    
    elif spec_str == "SrbRegexpTokenizer":
        return SrbRegexpWordTokenizer()
    
    elif spec_str == "None":
        return DummyTokenizer()
    
    else:
        assert False, "Unknown tokenizer type: %s" % spec_str


if __name__ == "__main__":
    args = parse_args()

    sent_tokenizer = create_sent_tokenizer(args.sent_tokenizer)
    word_tokenizer = create_word_tokenizer(args.word_tokenizer)

    tokenizer = CascadeTokenizer(sent_tokenizer, word_tokenizer)

    istream = sys.stdin
    if args.in_text:
        istream = open(args.in_text, 'r', encoding='utf-8')

    ostream = sys.stdout
    if args.tokenized_text:
        ostream = open(args.tokenized_text, 'w', encoding='utf-8')
    
    if args.sent_per_line:
        tokenized_text = tokenize_stream_sent_per_line(istream, tokenizer)
    else:
        tokenized_text = tokenize_stream(istream, tokenizer)
    ostream.write(tokenized_text)
