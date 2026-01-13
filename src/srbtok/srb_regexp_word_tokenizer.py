import re
from nltk.tokenize import RegexpTokenizer
from .utils import normalize_text



def re_esc(regex_str, ignore_pipe=True):
    regex_str = re.escape(regex_str)
    if ignore_pipe:
        regex_str = regex_str.replace(r'\|', r'|')
    return regex_str


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
        braces_str = re_esc(r'()[]{}<>')
        braces = rf'(?:[{braces_str}])'

        # dot at the end of the quoted sentence should be separated from closing quotes
        quoted_eos_dot = r'\.(?="|\'\')'

        # emoji is one word
        emoji = re_esc(r':)|:(|;)|:-)|:-(')

        # 1 character
        quotes_1ch_str = r'"\''
        quotes_1ch = rf'(?:[{quotes_1ch_str}])'

        # 2 char quotes
        quotes_2ch = r'(?:\'\')'

        # longer quotes first to give them priority
        quotes = r'|'.join([quotes_2ch, quotes_1ch]) 

        # punctuation no dot - eos dot handled separately, dot inside sentence is not punctuation
        punct_str = re_esc('!|?|:|-|!|;')
        punct = re_esc(rf'(?:[{punct_str}])')

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
        return super(SrbRegexpWordTokenizer, self).span_tokenize(normalize_text(text))


    def tokenize(self, text):
        return [text[start:end] for start, end in self.span_tokenize(text)]
