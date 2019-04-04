


from dcard.api import api, route

class Post():
    def __init__(self, metadata=None):
        pass
    def get(self, content=True, links=True):
        _content = self.gen_content_reqs(self.ids) if content else []

    def gen_content_reqs(self, post_ids):
        return (api.get_post(post_id) for post_id in post_ids)
    def gen_links_reqs(self, post_ids):
        return (api.get_post_links(post_id) for post_id in post_ids)


class PostsResult:
    def __init__(self, generator):

        self.results = generator()

    def result(self):
        self.results = list(self.results)
        return self.results




post = Post()
# 231016024/links
req = post.gen_content_reqs([231016024])
# print(req)


# 目前  PostsResult 放最底下好像會出錯 不確定 
