from mendeley_client import MendeleyClient
import cPickle as pickle


mendeley = MendeleyClient('e85bfd505c149d2ab7b2516b3f524a69050202682', 'b90e70f2e369bac1ba944b4fca621d9d')

try:
    mendeley.load_keys()
except IOError:
    mendeley.get_required_keys()
    mendeley.save_keys()

groupId = '2058663'

print sorted(mendeley.__dict__.keys())
response = mendeley.group_documents(groupId, items=1000)
docs = response['document_ids']
print docs

all_docs = {}
for doc in docs:
    response = mendeley.group_doc_details(groupId, doc)
    url = response['mendeley_url']
    all_docs[url] = response
    print url, response

pickle.dump(all_docs, open('group_docs.pkl', 'w'))