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
}

trans_table = str.maketrans(trans_dict)

def normalize_text(text):
    return text.translate(trans_table)
