# coding=utf-8
import os
from textocat.api import TextocatApi, Document

api = TextocatApi('AUTH_TOKEN')  # put your AUTH_TOKEN here

# Getting API Status
status = api.status()
print(status.message)

# Sending document for entity recognition
txt = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ex01.txt')
with open(txt) as f:
    document = Document(f.read(), tag='hockey')

batch_status = api.entity_queue([document])
print(batch_status.batch_id, batch_status.status)

# Request batch status
batch_status2 = api.entity_request(batch_status.batch_id)
print(batch_status2.batch_id, batch_status2.status)

# Retrieve recognized doc
# Probably you should wait before call this to give the service time for entity recognition
batch = api.entity_retrieve([batch_status.batch_id])

# Search
search_result = api.entity_search('PERSON:Малкин')