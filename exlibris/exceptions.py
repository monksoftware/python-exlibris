# -*- coding: utf-8 -*-

import requests


class BookPurchaseError(requests.exceptions.HTTPError):

    def __init__(self, *args, **kwargs):
        response_text = kwargs['response'] if 'response' in kwargs else None
        message = (
            'Exlibris returned 400 ("Bad Request") for the purchase request.')
        if response_text:
            message += ' Error message: {}'.format(response_text)
        else:
            message += (
                ' There is no specific error message, probably an invalid'
                ' book ISBN or one of the other parameters')
        super(BookPurchaseError, self).__init__(message, **kwargs)
