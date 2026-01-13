def shift_spans_by_offset(spans, offset):
    for i in range(0, len(spans)):
        spans[i] = (spans[i][0] + offset, spans[i][1] + offset)
    return spans



class CascadeTokenizer:
    '''
    Combines sentence and word tokenizer into one:
      - We first run sentence tokenizer to get sentence boundaries.
      - Then segment each sentence by running word tokenizer to get word boundaries.

    The only requirement for tokenizers that will be combined is that they implement span_tokenize(text) method.
    '''
    def __init__(self, sent_tokenizer, word_tokenizer):
        self._sent_tokenizer = sent_tokenizer
        self._word_tokenizer = word_tokenizer
    

    def _sentence_word_segments(self, text, sent_span):
        sent_start, sent_end = sent_span
        sent = text[sent_start:sent_end]
        word_spans = list(self._word_tokenizer.span_tokenize(sent))
        shift_spans_by_offset(word_spans, sent_start)
        return word_spans


    def span_tokenize_sentences(self, text):
        '''
        Run sentence tokenizer only to get sentence spans.
        
        :param text: Input text
        returns: List of (start, end) pairs that represent sentence spans. Sentence is text[start:end].
        '''
        return list(self._sent_tokenizer.span_tokenize(text))


    def span_tokenize_words(self, text):
        '''
        Run word tokenizer only to get word spans.
        
        :param text: Input text
        returns: List of (start, end) pairs that represent word spans. Word is text[start:end].
        '''
        return list(self._word_tokenizer.span_tokenize(text))


    def span_tokenize(self, text):
        '''
        Run cascade of sentence tokenizer and word tokenizer and return word spans.
        
        :param text: Input text
        returns: List of (start, end) pairs that represent word spans. Word is text[start:end].
        '''
        sent_segments = self._sent_tokenizer.span_tokenize(text)
        word_segments = []
        for sent_span in sent_segments:
            word_segments.extend(self._sentence_word_segments(text, sent_span))
        return word_segments
