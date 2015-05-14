import json
from unittest import TestCase

import httpretty

from textocat.api import TextocatApi, Document, BatchStatus, AnnotatedDocument, Entity
from textocat.api import BASE_URL

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def _request_url(endpoint):
    return '?'.join([urljoin(BASE_URL, endpoint), 'auth_token=AUTH_TOKEN'])


class TextocatApiTestCase(TestCase):
    def setUp(self):
        self.api = TextocatApi('AUTH_TOKEN')

    @httpretty.activate
    def test_status(self):
        httpretty.register_uri(httpretty.GET, _request_url('status'),
                               body='{\n"message": "The service is operating normally",\n"statusCode": "200 OK"\n}',
                               status=200,
                               content_type='application/json')
        status = self.api.status()
        self.assertEqual('200 OK', status.status_code)
        self.assertEqual('The service is operating normally', status.message)

    @httpretty.activate
    def test_entity_queue(self):
        batch_id = 'BA193147-04BB-49B1-BE91-0D4AAEF83F99'
        httpretty.register_uri(httpretty.POST, _request_url('entity/queue'),
                               body='{\n"batchId":"' + batch_id + '",\n"status": "' + BatchStatus.IN_PROGRESS + '"\n}',
                               status=202,
                               content_type='application/json')
        documents = [Document("Hello, World!", tag="test")]
        batch_status = self.api.entity_queue(documents)
        self.assertEqual(batch_id, batch_status.batch_id)
        self.assertEqual(BatchStatus.IN_PROGRESS, batch_status.status)

    @httpretty.activate
    def test_entity_request(self):
        batch_id = 'BA193147-04BB-49B1-BE91-0D4AAEF83F99'
        httpretty.register_uri(httpretty.GET, _request_url('entity/request'),
                               body='{\n"batchId":"' + batch_id + '",\n"status": "' + BatchStatus.FINISHED + '"\n}',
                               status=200,
                               content_type='application/json')
        batch_status = self.api.entity_request(batch_id)
        self.assertEqual(batch_id, batch_status.batch_id)
        self.assertEqual(BatchStatus.FINISHED, batch_status.status)

    @httpretty.activate
    def test_entity_retrieve(self):
        batch_id = 'BA193147-04BB-49B1-BE91-0D4AAEF83F99'
        result = {
            'batchIds': [
                batch_id
            ],
            'documents': [
                {
                    'status': AnnotatedDocument.SUCCESS,
                    'tag': 'test',
                    'entities': [
                        {
                            'span': 'World',
                            'beginOffset': 7,
                            'endOffset': 11,
                            'category': Entity.LOCATION
                        }
                    ]
                }
            ]
        }
        httpretty.register_uri(httpretty.GET, _request_url('entity/retrieve'),
                               body=json.dumps(result),
                               status=200,
                               content_type='application/json')

        batch = self.api.entity_retrieve(batch_id)
        self.assertItemsEqual([batch_id], batch.batch_ids)
        self.assertEqual(1, len(batch.documents))

        doc = batch.documents[0]
        self.assertEqual(AnnotatedDocument.SUCCESS, doc.status)
        self.assertEqual('test', doc.tag)
        self.assertEqual(1, len(doc.entities))

        entity = doc.entities[0]
        self.assertEqual('World', entity.span)
        self.assertEqual(7, entity.begin_offset)
        self.assertEqual(11, entity.end_offset)
        self.assertEqual(Entity.LOCATION, entity.category)

    @httpretty.activate
    def test_entity_search(self):
        query = 'World'
        result = {
            'searchQuery': query,
            'documents': [
                {
                    'status': AnnotatedDocument.SUCCESS,
                    'tag': 'test',
                    'entities': [
                        {
                            'span': 'World',
                            'beginOffset': 7,
                            'endOffset': 11,
                            'category': Entity.LOCATION
                        }
                    ]
                }
            ]
        }
        httpretty.register_uri(httpretty.GET, _request_url('entity/search'),
                               body=json.dumps(result),
                               status=200,
                               content_type='application/json')

        search_result = self.api.entity_search('hello')
        self.assertEqual(query, search_result.search_query)
        self.assertEqual(1, len(search_result.documents))

        doc = search_result.documents[0]
        self.assertEqual(AnnotatedDocument.SUCCESS, doc.status)
        self.assertEqual('test', doc.tag)
        self.assertEqual(1, len(doc.entities))

        entity = doc.entities[0]
        self.assertEqual('World', entity.span)
        self.assertEqual(7, entity.begin_offset)
        self.assertEqual(11, entity.end_offset)
        self.assertEqual(Entity.LOCATION, entity.category)


