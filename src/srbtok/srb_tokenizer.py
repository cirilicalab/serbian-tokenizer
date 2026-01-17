from nltk.tokenize import PunktSentenceTokenizer, RegexpTokenizer
from .cascade_tokenizer import CascadeTokenizer
import re
import os
import pickle


# ##########################################################################
# Text normalization 
# ##########################################################################

# transliteration table which maps different variants of quotes, punctuations to the most common variant
trans_dict = {
    '\xa0' : ' ',   # non breaking space to regular space
    '„' : '"',      # different double quotes to ascii double quote
    '“' : '"',            
    '”' : '"',
    'ˮ' : '"',
    '’' : "'",      # different single quotes to ascii single quote
    '‚' : "'",
    '‘' : "'",
    '0' : '0',      # all digits become 0 so all numbers are treated based on number of digits only (needed for sentence tokenizer)
    '1' : '0',
    '2' : '0',
    '3' : '0',
    '4' : '0',
    '5' : '0',
    '6' : '0',
    '7' : '0',
    '8' : '0',
    '9' : '0',
}
trans_table = str.maketrans(trans_dict)


def normalize_text(text):
    return text.translate(trans_table)


class NormPunktTokenizer(PunktSentenceTokenizer):
    '''
    Wrapper around NLTK PunktSentenceTokenizer which normalizes characters by calling utils.normalize().
    
    Purpose of normalization is to handle rare types of space, quotas, ... better by replacing them
    with similar characters that behave the same as far as sentence segmentation and word segmentations are
    concerned.

    For best performance, the training data for PunktTokenizer should be normalized as well.
    '''
    def __init__(self, *args, **kwargs):
        super(NormPunktTokenizer, self).__init__(*args, **kwargs)
    

    def span_tokenize(self, text):
        return super(NormPunktTokenizer, self).span_tokenize(normalize_text(text))
    

    def tokenize(self, text):
        return [text[start:end] for start, end in self.span_tokenize(text)]



# ##########################################################################
# Serbian sentence tokenization
# ##########################################################################


def create_serbian_punkt_tokenizer():
    '''
    Loads serbian punkt tokenizer from picke came with this module.
    '''
    script_dir = os.path.dirname(os.path.realpath(__file__))
    srb_pickle = os.path.join(script_dir, "serbian_punkt_nltk.pickle")
    with open(srb_pickle, 'rb') as f:
        params = pickle.load(f)
        return NormPunktTokenizer(params)



def _re_esc(regex_str, ignore_pipe=True):
    '''Helper method that escapes characters in reges, except for |.'''
    regex_str = re.escape(regex_str)
    if ignore_pipe:
        regex_str = regex_str.replace(r'\|', r'|')
    return regex_str


# ##########################################################################
# Serbian word tokenization
# ##########################################################################

class SrbRegexpWordTokenizer(RegexpTokenizer):
    '''
    Serbian word tokenizer based on handcrafted regular expressions. This tokenizer can't handle sentence segmentation and therefore should
    be used in cascade with tokenizer specialized for sentence segmentation.
    '''
    def __init__(self):
        # words and abbreviations (option dot)
        word = r'\w+\.?(?=\s+[^\s])'

        # last word in the sentence can't be abbreviation
        last_word = r'\w+'

        # dot at the end of the sentence (could be multiple)
        eos_dot = r'\.+$'

        # three dots is a single word
        three_dots = r'…|\.\.\.'

        # unicode email address
        email = r'\w+@\w+\.(?:\w\w\w?)'

        # url
        url = r'(?:http://|https://)?\w+(?:\.\w+)+'

        # date
        date = r'\d?\d\.\d?\d\.(?:\d\d\d\d|\d\d)?\.?'

        # braces should be treated as words
        braces_str = _re_esc(r'()[]{}<>')
        braces = rf'(?:[{braces_str}])'

        # dot at the end of the quoted sentence should be separated from closing quotes
        quoted_eos_dot = r'\.(?="|\'\')'

        # emoji is one word
        emoji = _re_esc(r':)|:(|;)|:-)|:-(')

        # 1 character
        quotes_1ch_str = r'"\''
        quotes_1ch = rf'(?:[{quotes_1ch_str}])'

        # 2 char quotes
        quotes_2ch = r'(?:\'\')'

        # longer quotes first to give them priority
        quotes = r'|'.join([quotes_2ch, quotes_1ch]) 

        # punctuation no dot - eos dot handled separately, dot inside sentence is not punctuation
        punct_str = _re_esc('!|?|:|-|!|;')
        punct = _re_esc(rf'(?:[{punct_str}])')

        # all other characters should be grouped in spans (other = no letters, no digits, no quotes)
        other_chars = rf'[^\w\s\.{quotes_1ch_str}{braces_str}]+'

        # decimal numbers, dot at the end for ordinal numbers
        decimal_number_srb = r'\-?\d+(?:\.\d\d\d+)*(?:,\d+)?(?=\s)'
        decimal_number_usa = r'\-?\d+(?:\,\d\d\d+)*(?:.\d+)?(?=\s)'
        ordinal_number = r'\d+\.(?=\s)'
        number = r'|'.join([ordinal_number, decimal_number_srb, decimal_number_usa])
        # abbreviation inflections
        # abbrev_inf_only_str = r'ових|овог|овом|овим|овој|ове|ова|ову|ови|ом|ов|ја|ју|а|у|е|и'

        # do not break on dash (could be multiple)
        word_with_dash=r'\w+(?:\-\w+)+'

        # need to support time formats
        # 8:01,67 минута
        # 
        
        # this rule will catch any non blank character that other rules missed and declare it as word token
        catch_any = r'[^\s]'

        # regex pattern is union of all of above groups
        pattern = r'|'.join([number, word_with_dash, word, date, quotes, three_dots, email, url, emoji, braces, punct, other_chars, last_word, eos_dot, quoted_eos_dot, catch_any])
        super(SrbRegexpWordTokenizer, self).__init__(pattern)


    def span_tokenize(self, text):
        '''Produces list of sentence segment spans (start, end). Where sentence is text[start:end].'''
        return super(SrbRegexpWordTokenizer, self).span_tokenize(normalize_text(text))


    def tokenize(self, text):
        '''Returns list of sentence strings.'''
        return [text[start:end] for start, end in self.span_tokenize(text)]


# ##########################################################################
# Serbian tokenizer
# ##########################################################################

class SrbTokenizer(CascadeTokenizer):
    '''Tokenizer for SerbianCyrillic. This is what you want to use to tokenize the text.'''
    def __init__(self):
        super(SrbTokenizer, self).__init__(create_serbian_punkt_tokenizer(), SrbRegexpWordTokenizer())

