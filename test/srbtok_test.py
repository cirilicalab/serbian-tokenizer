import unittest
from srbtok.srb_tokenizer import SrbRegexpWordTokenizer


class SrbRegexpTokenizerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SrbRegexpTokenizerTest, self).__init__(*args, **kwargs)
        self.tokenizer = SrbRegexpWordTokenizer()

    def test_split_on_space(self):
        tokens = list(self.tokenizer.tokenize("Клиперси савладали Нетсе"))
        self.assertEqual(["Клиперси","савладали", "Нетсе"], tokens)

    def test_keep_abbreviation(self):
        tokens = list(self.tokenizer.tokenize("Др. Милован Илић"))
        self.assertEqual(["Др.","Милован", "Илић"], tokens)

        # non letter character following space after ordinal number (also handled by abbreviation regex)
        tokens = list(self.tokenizer.tokenize("Запажени 2004. )"))
        self.assertEqual(["Запажени", "2004.", ")"], tokens)

    def test_split_dot_at_eos(self):
        tokens = list(self.tokenizer.tokenize("Др. Милован Илић."))
        self.assertEqual(["Др.","Милован", "Илић", "."], tokens)

    def test_split_punct(self):
        tokens = list(self.tokenizer.tokenize("Учествовали су: Др. Милован Илић, Др. Цане, Др. Ана."))
        self.assertEqual(["Учествовали", "су", ":", "Др.", "Милован", "Илић", ",", "Др.", "Цане", ",", "Др.", "Ана", "."], tokens)

    def test_split_quotes(self):
        tokens = list(self.tokenizer.tokenize("\"Наш тим је победио!\", узвикнуо је."))
        self.assertEqual(["\"", "Наш", "тим", "је", "победио", "!", "\"", ",", "узвикнуо", "је", "."], tokens)

        tokens = list(self.tokenizer.tokenize("'Наш тим је победио!', узвикнуо је."))
        self.assertEqual(["'", "Наш", "тим", "је", "победио", "!", "'", ",", "узвикнуо", "је", "."], tokens)

    def test_split_other(self):
        tokens = list(self.tokenizer.tokenize("јабука%$#"))
        self.assertEqual(["јабука", "%$#"], tokens)

    def test_number(self):
        tokens = list(self.tokenizer.tokenize("Крушке 100 дин."))
        self.assertEqual(["Крушке", "100", "дин", "."], tokens)

        tokens = list(self.tokenizer.tokenize("Крушке 100.50 дин."))
        self.assertEqual(["Крушке", "100.50", "дин", "."], tokens)

        tokens = list(self.tokenizer.tokenize("Крушке 100,50 дин."))
        self.assertEqual(["Крушке", "100,50", "дин", "."], tokens)

        tokens = list(self.tokenizer.tokenize("Крушке 1.000.000,50 дин."))
        self.assertEqual(["Крушке", "1.000.000,50", "дин", "."], tokens)

        tokens = list(self.tokenizer.tokenize("Најнижа температура од -5 до 0 степени, а највиша од -1 до 4 степена."))
        self.assertEqual(["Најнижа", "температура", "од", "-5", "до", "0", "степени", ",", "а", "највиша", "од", "-1", "до", "4", "степена", "."], tokens)


    def test_split_quoted_eos_dot(self):
        tokens = list(self.tokenizer.tokenize("\"Наш тим је победио.\", узвикнуо је."))
        self.assertEqual(["\"", "Наш", "тим", "је", "победио", ".", "\"", ",", "узвикнуо", "је", "."], tokens)

        tokens = list(self.tokenizer.tokenize("„Наш тим је победио.“, узвикнуо је."))
        self.assertEqual(["„", "Наш", "тим", "је", "победио", ".", "“", ",", "узвикнуо", "је", "."], tokens)

        tokens = list(self.tokenizer.tokenize("‚Наш тим је победио.‘, узвикнуо је."))
        self.assertEqual(["‚", "Наш", "тим", "је", "победио", ".", "‘", ",", "узвикнуо", "је", "."], tokens)

    def test_other_char_eos(self):
        tokens = list(self.tokenizer.tokenize("имена: "))
        self.assertEqual(["имена", ":"], tokens)

        tokens = list(self.tokenizer.tokenize("имена:"))
        self.assertEqual(["имена", ":"], tokens)

    def test_alt_quotes(self):
        tokens = list(self.tokenizer.tokenize("''Наш тим је победио.'', узвикнуо је."))
        self.assertEqual(["''", "Наш", "тим", "је", "победио", ".", "''", ",", "узвикнуо", "је", "."], tokens)


    def test_ordinal_number(self):
        tokens = list(self.tokenizer.tokenize("1. Арина Сабаленка"))
        self.assertEqual(["1.", "Арина", "Сабаленка"], tokens)


    def test_three_dots(self):
        tokens = list(self.tokenizer.tokenize("Јабуке..."))
        self.assertEqual(["Јабуке", "..."], tokens)

        tokens = list(self.tokenizer.tokenize("Јабуке... крушке"))
        self.assertEqual(["Јабуке", "...", "крушке"], tokens)

    def test_three_braces(self):
        tokens = list(self.tokenizer.tokenize("((јабука))"))
        self.assertEqual(["(", "(", "јабука", ")", ")"], tokens)


    def test_emoji(self):
        tokens = list(self.tokenizer.tokenize("здраво :)"))
        self.assertEqual(["здраво", ":)"], tokens)

        tokens = list(self.tokenizer.tokenize("здраво:)"))
        self.assertEqual(["здраво", ":)"], tokens)

        tokens = list(self.tokenizer.tokenize("здраво:-("))
        self.assertEqual(["здраво", ":-("], tokens)

    def test_repeated_punct(self):
        tokens = list(self.tokenizer.tokenize("супер!!!!"))
        self.assertEqual(["супер", "!", "!", "!", "!"], tokens)


    def test_email(self):
        tokens = list(self.tokenizer.tokenize("имејл myemail@host.com"))
        self.assertEqual(["имејл", "myemail@host.com"], tokens)
        
        tokens = list(self.tokenizer.tokenize("имејл myemail@host.rs"))
        self.assertEqual(["имејл", "myemail@host.rs"], tokens)

        tokens = list(self.tokenizer.tokenize("имејл миле@шампиони.срб"))
        self.assertEqual(["имејл", "миле@шампиони.срб"], tokens)


    def test_url(self):
        tokens = list(self.tokenizer.tokenize("www.host.com"))
        self.assertEqual(["www.host.com"], tokens)

        tokens = list(self.tokenizer.tokenize("http://www.host.com"))
        self.assertEqual(["http://www.host.com"], tokens)

        tokens = list(self.tokenizer.tokenize("https://www.host.com"))
        self.assertEqual(["https://www.host.com"], tokens)


    def test_date(self):
        tokens = list(self.tokenizer.tokenize("01.01.2025."))
        self.assertEqual(["01.01.2025."], tokens)

        tokens = list(self.tokenizer.tokenize("01.01.2025"))
        self.assertEqual(["01.01.2025"], tokens)

        tokens = list(self.tokenizer.tokenize("01.01."))
        self.assertEqual(["01.01."], tokens)

        tokens = list(self.tokenizer.tokenize("1.1.2025"))
        self.assertEqual(["1.1.2025"], tokens)


    def test_words_with_dash(self):
        tokens = list(self.tokenizer.tokenize("РТС-а"))
        self.assertEqual(["РТС-а"], tokens)

        tokens = list(self.tokenizer.tokenize("3-Д"))
        self.assertEqual(["3-Д"], tokens)

        tokens = list(self.tokenizer.tokenize("Би-Би-Си"))
        self.assertEqual(["Би-Би-Си"], tokens)

        tokens = list(self.tokenizer.tokenize("10-годишњак"))
        self.assertEqual(["10-годишњак"], tokens)



if __name__ == '__main__':
    unittest.main()
