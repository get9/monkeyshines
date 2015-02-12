import urllib.parse
import requests
import logging
import re

def fetch(urlo, cookies=None, t=5):
    if not re.match('https?:\/\/', urlo.url):
        if re.match('\/\/', urlo.url):
            urlo.url = 'http:' + urlo.url
        else:
            urlo.url = 'http://' + urlo.url

    logging.info("Fetching {}".format(urlo.url))
    try:
        resp = requests.get(urlo.url, cookies=cookies, timeout=t, allow_redirects=True)
    except requests.exceptions.Timeout:
        logging.debug("Received timeout exception", exc_info=True)
        # Set that URL was timed out, and remove status code.
        urlo.timedout = True
        urlo.status_code = None
        return None
    except requests.exceptions.SSLError:
        logging.debug("Received SSL exception", exc_info=True)
        urlo.status_code = None
        return None
    except requests.exceptions.ConnectionError:
        logging.debug("Received ConnectionError exception", exc_info=True)
        urlo.status_code = None
        return None
    except requests.exceptions.TooManyRedirects:
        logging.debug("Received TooManyRedirects exception", exc_info=True)
        urlo.status_code = None
        return None
    except requests.exceptions.InvalidURL:
        logging.debug("Received InvalidURL exception", exc_info=True)
        urlo.status_code = None
        return None
    urlo.status_code = resp.status_code
    return resp
