from functools import partialmethod

from dcard.utils import Client

class API():
    def __init__(self):
        self.client = Client()

    def get_all_forums(self):
        return self.client.get_json(route.forums())

    def get_general_forums(self):
        forums = self.client.get_json(route.forums())
        return [forum for forum in forums if not forum['isSchool']]

    def get_post(self, post_id, addition=None, params=None):
        # print(route.post(post_id, addition=addition))
        req = self.client.get(route.post(post_id, addition=addition), params=params)
        return req

    get_post_links = partialmethod(get_post, addition='links')

class Route():
    host = 'https://www.dcard.tw/'
    def forums(self):
        return Route.host + '_api/forums'
    # ex: https://www.dcard.tw/_api/forums/pet/posts?popular=true&limit=30
    def posts_meta(self, forums):
        return self.forums() + '/{}/posts'.format(forums)
    def post(self, post_id, addition=None):
        base = Route.host + '_api/posts/{id}'.format(id=post_id)
        if addition:
            return base + '/' + addition
        return base

    post_links = partialmethod(post, addition='links')
    post_comments = partialmethod(post, addition='comments')


route = Route()
# print(route.post_links(231016024))
api = API()
res = api.get_post(231016024)
# print(res)

# ex: post_id 231016024