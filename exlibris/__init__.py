from __future__ import absolute_import
from __future__ import unicode_literals
import hashlib
import hmac
import time
import uuid

import requests

from . import exceptions


class ExlibrisClient():

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.start_url = 'https://exlibris.bookrepublic.it/api/{}/'.format(
            self.key)
        self.endpoints = self.get_features()

    def _build_message_to_sign(self, **data):
        return (
            ''.join('{}{}'.format(k, v) for k, v in sorted(data.items()))
            .encode('utf-8'))

    def _send_request(self, method, url, query_params=None, body_data=None):
        if query_params is None:
            query_params = {}
        if body_data is None:
            body_data = {}

        required_query_params = {
            'timestamp': str(int(time.time())),
            'marker': str(uuid.uuid4()),
        }
        data = {}
        data.update(query_params)
        data.update(body_data)
        data.update(required_query_params)
        message = self._build_message_to_sign(**data)
        signature = hmac.new(self.secret, message, digestmod=hashlib.sha1)
        required_query_params['sig'] = signature.hexdigest()
        all_query_params = dict(query_params, **required_query_params)
        return requests.request(
            method, url, params=all_query_params, data=body_data)

    def get_features(self):
        return self._send_request('GET', self.start_url).json()

    def buy_ebook(self, isbn, buyer_transaction_id, customer_name, price,
                  customer_email=None, message=None,tags=None):
        data = {
            'isbn': isbn,
            'buyer_transaction_id': buyer_transaction_id,
            'customer_name': customer_name,
            'price': price,
        }
        if customer_email:
            data['customer_email'] = customer_email
        if message:
            data['message'] = message
        if tags:
            data['tags'] = tags

        response = self._send_request(
            'POST', self.endpoints['transactions'], body_data=data)
        # it seems like if an invalid ISBN is supplied, exlibris
        # returns 400 without any error message
        if response.status_code == 400:
            raise exceptions.BookPurchaseError(response=response)
        if not response.ok:
            raise requests.HTTPError
        return response.json()
