from unittest import TestCase, main
from tax_resolve import tax_resolve
from get_mendeley_data import get_mendeley_data, citation


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
        self.urls = [
                     "http://www.mendeley.com/research/niche-neutrality/",
                     "http://www.mendeley.com/research/local-interactions-select-lower-pathogen-infectivity/",
                     "http://www.mendeley.com/research/widespread-amphibian-extinctions-epidemic-disease-driven-global-warming/",
                     ]

        self.data_docs = []
        self.citations = []
        for url in self.urls:
            self.data_docs.append(get_mendeley_data(url))
            self.citations.append(citation(url))

        print '\n\n'.join(self.citations)

    def test_mendeley_tags(self):
        data_doc = self.data_docs[0]
        citation = self.citations[0]
        self.assertEqual(data_doc['title'], 'A niche for neutrality')
        self.assertEqual(data_doc['year'], 2007)
        self.assertEqual(data_doc['published_in'], 'Ecology Letters')
        self.assertIn('Adler, P. B.', citation)
        self.assertIn(data_doc['title'], citation)

        data_doc = self.data_docs[1]
        citation = self.citations[1]
        self.assertEqual(data_doc['title'], 'Local interactions select for lower pathogen infectivity')
        self.assertEqual(data_doc['year'], 2007)
        self.assertEqual(data_doc['published_in'], 'Science')
        self.assertIn('Boots, M.', citation)
        self.assertIn(data_doc['title'], citation)

        data_doc = self.data_docs[2]
        citation = self.citations[2]
        self.assertEqual(data_doc['title'], 'Widespread amphibian extinctions from epidemic disease driven by global warming')
        self.assertEqual(data_doc['year'], 2006)
        self.assertEqual(data_doc['published_in'], 'Nature')
        self.assertIn('Pounds, J. A.', citation)
        self.assertIn(data_doc['title'], citation)


if __name__ == '__main__':
    main()