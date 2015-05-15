# coding=utf-8
import requests
from textocat.exceptions import raise_by_http_code
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

BASE_URL = 'http://api.textocat.com/'


class ApiStatus(object):
    """

    """

    def __init__(self, status_code, message):
        """
        """
        self.message = message
        self.status_code = status_code

    @staticmethod
    def from_json(json):
        return ApiStatus(json.get('statusCode'), json.get('message'))


class BatchStatus(object):
    """

    """
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'

    def __init__(self, batch_id, status):
        """
        """
        self.batch_id = batch_id
        self.status = status

    @staticmethod
    def from_json(json):
        """
        """
        return BatchStatus(json.get('batchId'), json.get('status'))


class Batch(object):
    """

    """

    def __init__(self, batch_ids, documents):
        """
        """
        self.batch_ids = batch_ids
        self.documents = documents

    @staticmethod
    def from_json(json):
        """
        """
        return Batch(json.get('batchIds'),
                     [AnnotatedDocument.from_json(doc) for doc in json.get('documents')])


class Document(object):
    """

    """

    def __init__(self, text, tag=''):
        """
        """
        self.text = text
        self.tag = tag

    def to_dict(self):
        """
        """
        return {'text': self.text, 'tag': self.tag}

    @staticmethod
    def from_json(json):
        """
        """
        return Document(json.get('text'), json.get('tag'))


class AnnotatedDocument(object):
    """

    """
    SUCCESS = 'SUCCESS'
    INPUT_ERROR = 'INPUT_ERROR'
    SERVICE_ERROR = 'SERVICE_ERROR'

    def __init__(self, status, entities, tag=''):
        """
        """
        self.status = status
        self.entities = entities
        self.tag = tag


    @staticmethod
    def from_json(json):
        """
        """
        return AnnotatedDocument(json.get('status'),
                                 [Entity.from_json(e) for e in json.get('entities')],
                                 tag=json.get('tag', ''))


class Entity(object):
    """

    """
    PERSON = 'PERSON'
    ORGANIZATION = 'ORGANIZATION'
    GPE = 'GPE'
    LOCATION = 'LOCATION'
    TIME = 'TIME'
    MONEY = 'MONEY'

    def __init__(self, span, begin_offset, end_offset, category):
        """
        """
        self.span = span
        self.begin_offset = begin_offset
        self.end_offset = end_offset
        self.category = category

    @staticmethod
    def from_json(json):
        """
        """
        return Entity(json.get('span'),
                      json.get('beginOffset'),
                      json.get('endOffset'),
                      json.get('category'))


class SearchResult(object):
    """
    """

    def __init__(self, search_query, documents):
        """
        """
        self.search_query = search_query
        self.documents = documents

    @staticmethod
    def from_json(json):
        """
        """
        return SearchResult(json.get('searchQuery'),
                            [AnnotatedDocument.from_json(doc) for doc in json.get('documents')])


class TextocatApi(object):
    """
    TextocatApi
    """

    def __init__(self, auth_token):
        """
        :param auth_token:
        :return:
        """
        self.auth_token = auth_token

    def _request_url(self, endpoint):
        """

        :param endpoint:
        :return:
        """
        return '?'.join([urljoin(BASE_URL, endpoint),
                         urlencode({'auth_token': self.auth_token})])

    def entity_queue(self, documents):
        """

        :param documents:
        :return:
        """
        r = requests.post(self._request_url('entity/queue'),
                          json=[x.to_dict() for x in documents])
        if r.status_code == requests.codes.accepted:
            json = r.json()
            return BatchStatus(json.get('batchId'), json.get('status'))

        raise_by_http_code(r.status_code)

    def entity_request(self, batch_id):
        """

        :param batch_id:
        :return:
        """
        r = requests.get(self._request_url('entity/request'),
                         params={'batch_id': batch_id})
        if r.status_code == requests.codes.ok:
            json = r.json()
            return BatchStatus(json.get('batchId'), json.get('status'))

        raise_by_http_code(r.status_code)

    def entity_retrieve(self, batch_ids):
        """
        :param batch_ids:
        :return:
        """
        r = requests.get(self._request_url('entity/retrieve'),
                         params={'batch_id': batch_ids})
        if r.status_code == requests.codes.ok:
            return Batch.from_json(r.json())

        raise_by_http_code(r.status_code)

    def entity_search(self, query):
        """
        :param query:
        :return:
        """
        r = requests.get(self._request_url('entity/search'),
                         params={'search_query': query})
        if r.status_code == requests.codes.ok:
            return SearchResult.from_json(r.json())

        raise_by_http_code(r.status_code)

    def status(self):
        """
        :return:
        """
        r = requests.get(self._request_url('status'))

        if r.status_code == requests.codes.ok:
            return ApiStatus.from_json(r.json())

        raise_by_http_code(r.status_code)


