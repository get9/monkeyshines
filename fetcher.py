import urlparse
import requests

def fetch(self, urlo, cookies=None, t=20):
    try:
        resp = requests.get('http://' + urlo.url, cookies=cookies, timeout=t,
                            allow_redirects=True)
    except requests.exceptions.Timeout:
        # Set that URL was timed out, and remove status code.
        urlo.timedout = True
        urlo.status_code = None
        return None
    return resp
