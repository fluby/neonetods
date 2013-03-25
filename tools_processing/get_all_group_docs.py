from mendeley_client import MendeleyClient
import cPickle as pickle

mendeley = MendeleyClient('f37044bebbda140b8ad9a7a923588a84051253aa2','0038b670aa7e4ec9e4aaf441599bec13')
##mendeley = MendeleyClient('<consumer_key>', '<secret_key>')
mendeley.load_keys()
data = pickle.load(open('mendeley_api_keys.pkl', 'rb'))

request_token = data['request_token']
access_token = data['access_token']

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

pickle.dump(all_docs, open('group_docs.pkl', 'wb'))