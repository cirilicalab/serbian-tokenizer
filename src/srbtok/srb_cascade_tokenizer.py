from .srb_regexp_word_tokenizer import SrbRegexpWordTokenizer
from .norm_punkt_tokenizer import create_serbian_punkt_tokenizer
import pickle

class SrbCascadeTokenizer:
    def __init__(self):
        sent_tokenizer = create_serbian_punkt_tokenizer()
        word_tokenizer = SrbRegexpWordTokenizer()
        super(SrbRegexpWordTokenizer, self).__init__(sent_tokenizer, word_tokenizer)
