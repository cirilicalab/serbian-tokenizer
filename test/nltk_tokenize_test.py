import unittest
import io

from tools.nltk_tokenize import * 

class TestNLTKTokenize(unittest.TestCase):
    def test_word_spans_to_segmented_text(self):
        text = "  a bc  def   "
        word_spans = [(2,3), (4,6), (8,11)]
        segmented_text = word_spans_to_tokenized_text(text, word_spans)

        expected = "a" + WORD_SEP + "bc" + WORD_SEP + "def"
        self.assertEqual(expected, segmented_text)

        text = "   "
        word_spans = []
        segmented_text = word_spans_to_tokenized_text(text, word_spans)
        self.assertEqual("", segmented_text)


    def test_tokenize_stream(self):
        tokenizer = create_word_tokenizer("WhitespaceTokenizer")
        input_string = """
        a bc  def  
          1

        2 456
        """

        stream = io.StringIO(input_string)
        segmented_text = tokenize_stream(stream, tokenizer)

        expected = """
a bc def
1

2 456
"""
        self.assertEqual(expected, segmented_text)


if __name__ == '__main__':
    unittest.main()
