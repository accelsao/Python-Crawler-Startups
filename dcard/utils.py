import requests
from . import prequests


class Client():
    def __init__(self):
        session = requests.Session()
        session.headers['User - Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        self.session = session

    def get_json(self, url):
        response = self.session.get(url)
        data = response.json()
        return data

    def get(self, url, **kwargs):
        return prequests.get(url, session=self.session, **kwargs)
