
# ##########################################################################
# Producing text with space separated tokens from list of word spans.
# ##########################################################################

WORD_SEP = ' '

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


# ##########################################################################
# Segmenting streams and files.
# ##########################################################################

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

