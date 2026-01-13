import os
import sys
import argparse

from nltk.tokenize import TreebankWordTokenizer, WhitespaceTokenizer, PunktTokenizer, ToktokTokenizer

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srbtok import SrbRegexpWordTokenizer, CascadeTokenizer, create_serbian_punkt_tokenizer

#
# Notes:
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


def check_space(text):
    for char in text:
        assert char.isspace(), "Space expected: '%s'" % text


def has_separator(text):
    return WORD_SEP in text


def word_spans_to_tokenized_text(text, word_spans, debug=False):
    '''
    Takes text and detected word boundaries and produces augmented text where each word is surrounded by start/end marker characters.
    
    :param text: Input text
    :param word_spans: Word boundaries as (start, end) offsets. Word is test[start:end]
    '''
    out_fragments = []
    
    offset = 0
    for start_offset, end_offset in word_spans:
        # verify input
        assert start_offset < end_offset
        assert offset <= start_offset

        # skip leading space
        if debug:
            check_space(text[offset:start_offset])

        # add word
        word = text[start_offset:end_offset]
        assert not has_separator(word), "Word separator character '%s' found inside word boundaries"
        out_fragments.append(word)

        # add word separator
        out_fragments.append(WORD_SEP)

        # move offset to the first char after the word
        offset = end_offset

    # word separator is not needed at the end of the string
    if len(out_fragments) > 0:
        assert out_fragments[-1] == WORD_SEP
        out_fragments.pop()

    # check tail space
    check_space(text[offset:])

    # concatenate all substrings
    return "".join(out_fragments)


def tokenize_stream(istream, tokenizer):
    '''
    Segment input stream line by line and return WORD_SEP separated word tokens.
    '''
    segmented_lines = []
    for line in istream:
        line = line.rstrip('\r\n')
        word_spans = list(tokenizer.span_tokenize(line))
        segmented_lines.append(word_spans_to_tokenized_text(line, word_spans))
    return "\n".join(segmented_lines)


def tokenize_stream_sent_per_line(istream, tokenizer):
    '''
    Segment input stream line by line and return WORD_SEP separated word tokens.
    '''
    segmented_lines = []
    for line in istream:
        line = line.rstrip('\r\n')
        for sent_start, sent_end in list(tokenizer.span_tokenize_sentences(line)):
            # get sentence
            sentence = line[sent_start:sent_end]
            
            # word spans for this sentence
            word_spans = list(tokenizer.span_tokenize_words(sentence))
        
            # generate segmented text line
            segmented_lines.append(word_spans_to_tokenized_text(sentence, word_spans))
    
    return "\n".join(segmented_lines)


def tokenize_file(path, tokenizer):
    with open(path, 'r', encoding='utf-8') as file:
        return tokenize_stream(file, tokenizer)


# def encode_multiline_str(multiline):
#     return multiline.replace(LINE_SEP, LINE_SEP_REPLACEMENT).replace('\n', LINE_SEP)


# def fix_relative_path(relative_path, base_dir):
#     '''
#     Fixes path which is relative to the base_dir.
    
#     :param relative_path: Path which is relative to the base_dir.
#     :param base_dir: Base dir.
#     '''
#     if os.path.isabs(relative_path):
#         return relative_path
#     return os.path.join(base_dir, relative_path)


# def read_filelist(list_path):
#     '''
#     Reads file with list of file paths. If path in the is relative it should be resolved as relative to the file list dir.
#     '''
#     file_paths = []
#     base_dir = os.path.dirname(list_path)
#     with open(list_path, 'r', encoding='utf-8') as paths_file:
#         for line in paths_file:
#             line = line.rstrip('\r\n')
#             file_paths.append(fix_relative_path(line, base_dir))
#     return file_paths


# def segment_file_list(in_list_path, out_tsv_stream, tokenizer):
#     '''
#     Tokenizes files one by one and writes TSV output: (in_filename, tokenized_text). To convert tokenized text to a single line we use LINE_SEP.
    
#     :param in_list_path: file with list of input file paths. Relative paths are resolved to the location of this file.
#     :param out_tsv_stream: 
#     :param tokenizer: nltk tokenizer object
#     '''
#     with open(in_list_path, 'r', encoding='utf-8') as in_list:
#         for text_path in in_list:
#             # get tokenize text in single line
#             tokenized_text = tokenize_file(text_path, tokenizer)
#             tokenized_text = encode_multiline_str(tokenized_text)

#             # get filename for tsv output
#             in_filename = os.path.basename(in_list_path)

#             out_tsv_stream.write("%s\n" % "\n".join([in_filename, tokenized_text]))


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
