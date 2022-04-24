#!/usr/bin/env python

 

try:

    # For Python 3.0 and later

    from urllib.request import urlopen

except ImportError:

    # Fall back to Python 2's urllib2

    from urllib2 import urlopen

 

import certifi

import json

 

def get_jsonparsed_data(url):

    """

    Receive the content of ``url``, parse it as JSON and return the object.

 

    Parameters

    ----------

    url : str

 

    Returns

    -------

    dict

    """

    response = urlopen(url, cafile=certifi.where())

    data = response.read().decode("utf-8")

    return json.loads(data)

 

url = ("https://financialmodelingprep.com/api/v3/income-statement/TSM?apikey=1ab72d7a22c03ae71689a45d61529c36")

print(get_jsonparsed_data(url))