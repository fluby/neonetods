from unittest import TestCase, main
from tax_resolve import get_synonyms, tax_resolve
from get_mendeley_data import get_mendeley_data, citation


class TestTaxResolve(TestCase):
    def setUp(self):
        self.syn1 = {'applb': 'apple', 'applc': 'apple', 'bannnna': 'banana'}

        self.syn2 = get_synonyms('../data/mosquito_synonyms.csv')

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
            new_name = tax_resolve(l, syns=self.syn1)
            new_name = new_name if new_name else l
            self.assertEqual(new_name, r)
    
    def test_mosquitos(self):
        for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
            self.assertEqual(tax_resolve(to_test, syns=self.syn2), 'Aedes clivis')


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
        for data_doc, citation, (title, year, published_in, in_citation) in zip(self.data_docs, self.citations,
        [
         ('A niche for neutrality', 2007, 'Ecology Letters', 'Adler, P. B.'),
         ('Local interactions select for lower pathogen infectivity', 2007, 'Science', 'Boots, M.'),
         ('Widespread amphibean extinctions from epidemic disease riven by global warming', 2006, 'Nature', 'Pounds, J. A.'),
        ]):
            self.assertEqual(data_doc['title'], title)
            self.assertEqual(data_doc['year'], year)
            self.assertEqual(data_doc['published_in'], published_in)
            self.assertIn('Adler, P. B.', in_citation)


if __name__ == '__main__':
    main()
