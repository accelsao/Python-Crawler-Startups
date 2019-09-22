# -*- coding: utf-8 -*-
from urllib.parse import urlencode, quote_plus

def url_encode(query):
    if isinstance(query, str):
        query = quote_plus(query)
    else:
        query = urlencode(query)
    query = query.replace('+', '%20')
    return query