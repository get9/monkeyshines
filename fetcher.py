import urllib.parse
import requests

def fetch(urlo, cookies=None, t=20):
    print("fetching: {}".format(urlo.url))
    try:
        resp = requests.get(urlo.url, cookies=cookies, timeout=t, allow_redirects=True)
    except requests.exceptions.Timeout:
        # Set that URL was timed out, and remove status code.
        urlo.timedout = True
        urlo.status_code = None
        return None
    return resp
