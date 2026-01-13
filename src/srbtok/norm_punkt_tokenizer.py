from nltk.tokenize import PunktSentenceTokenizer
from .utils import normalize_text
import os
import pickle

class NormPunktTokenizer(PunktSentenceTokenizer):
    def __init__(self, *args, **kwargs):
        super(NormPunktTokenizer, self).__init__(*args, **kwargs)
    

    def span_tokenize(self, text):
        return super(NormPunktTokenizer, self).span_tokenize(normalize_text(text))
    

    def tokenize(self, text):
        return [text[start:end] for start, end in self.span_tokenize(text)]


def create_serbian_punkt_tokenizer():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    srb_pickle = os.path.join(script_dir, "serbian_punkt_nltk.pickle")
    with open(srb_pickle, 'rb') as f:
        params = pickle.load(f)
        return NormPunktTokenizer(params)
