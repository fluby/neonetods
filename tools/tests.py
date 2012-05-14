from unittest import TestCase, main
from tax_resolve import tax_resolve
from get_mendeley_data import get_mendeley_data


class TestTaxResolve(TestCase):
    def setUp(self):
        self.syn1 = {'applb': 'apple', 'applc': 'apple', 'bannnna': 'banana'}

        self.syn2 = {}
        data_file = open("../data/mosquito_synonyms.csv", 'r')
        data_file.readline()
        for line in data_file:
            wrong, right, spid, ref = line.split(',')
            self.syn2[wrong] = right


    def test_apple(self):
        for l, r in [('appleb', 'apple'), 
                     ('applb', 'apple'), 
                     ('apple', 'apple'), 
                     ('a', 'a'),
                     ('ap', 'ap'), 
                     ('appl', 'apple'), 
                     ('bionan', 'bionan'), 
                     ('banann', 'banana'), 
                     ('bannans', 'banana'),
                     ]:
            self.assertEqual(tax_resolve(l, self.syn1), r)
    
    def test_mosquitos(self):
        for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
            self.assertEqual(tax_resolve(to_test, self.syn2), 'Aedes clivis')


class TestMendeleyTags(TestCase):
    def setUp(self):
        self.data_doc = get_mendeley_data("http://www.mendeley.com/research/niche-neutrality/")

    def test_adler(self):
        self.assertEqual(self.data_doc['title'], 'A niche for neutrality')
        self.assertEqual(self.data_doc['year'], 2007)
        self.assertEqual(self.data_doc['published_in'], 'Ecology Letters')


if __name__ == '__main__':
    main()