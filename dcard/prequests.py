from requests import Session
from functools import partial

class AsyncRequest(object):
    def __init__(self, method, url, **kwargs):
        self.url = url
        self.method = method
        self.session = kwargs.pop('session', None)
        if self.session is None:
            self.session = Session()
            self.session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        callback = kwargs.pop('callback', None)
        if callback:
            kwargs['hooks'] = {'response': callback}
        self.kwargs = kwargs
        self.response = None

get = partial(AsyncRequest, 'GET')
options = partial(AsyncRequest, 'OPTIONS')
head = partial(AsyncRequest, 'HEAD')
post = partial(AsyncRequest, 'POST')
put = partial(AsyncRequest, 'PUT')
patch = partial(AsyncRequest, 'PATCH')
delete = partial(AsyncRequest, 'DELETE')

# s = get('https://www.dcard.tw/_api/posts/231016024')
# print(s)
# for i in s:
#     print(i)

def request(method, url, **kwargs):
    return AsyncRequest(method, url, **kwargs)


#
# res = get('https://www.dcard.tw/_api/posts/231016024')
# print(res)