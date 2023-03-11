import httpx
import json
from tenacity import retry, stop_after_attempt

from .clean_html import clean_article_html
from .html_to_nodes import html_to_nodes
from TOKENS import TG_TOKEN

CREATE_PAGE_URL = "https://api.telegra.ph/createPage"

def prepare_data(title, nodes, author, author_url):
    content_json_string = json.dumps(nodes,separators=(',', ':'), ensure_ascii=False)
    data = {
        "title": title, 
        "content": content_json_string, 
        "access_token": TG_TOKEN,
        "author_name": author,
        "author_url": author_url,
    }
    return data

# @retry(stop=stop_after_attempt(5))
# async def create_page_from_nodes(title, nodes, author, author_url):
#     data = prepare_data(title, nodes, author, author_url)
#     async with httpx.AsyncClient() as client:
#         r = await client.post(CREATE_PAGE_URL, data = data)
#     if r.status_code == httpx.codes.ok:
#         response = r.json()
#         if response['ok']:
#             return [response['result']['url']]
#         elif response['error'] == 'CONTENT_TOO_BIG':
#             return 'CONTENT_TOO_BIG' # TODO: handle this 
#             # Can be triggered by: https://mp.weixin.qq.com/s/I3xKYwB4rEIdPxT6Qz39lw
#     else:
#         raise Exception

# look at the comment above for a simpler version of this function
async def create_page_from_nodes(title, nodes, author, author_url):
    @retry(stop=stop_after_attempt(5))
    async def _helper(nodes, todo, results):
        if nodes == [] and todo == []:
            return results
        data = prepare_data(title, nodes, author, author_url)
        async with httpx.AsyncClient() as client:
            r = await client.post(CREATE_PAGE_URL, data = data)
        if r.status_code == httpx.codes.ok:
            response = r.json()
            if response['ok']:
                results.append(response['result']['url'])
                return await _helper(todo, [], results)
            elif response['error'] == 'CONTENT_TOO_BIG':
                m = len(nodes) // 2 # ignore the case of len == 1
                left = nodes[:m]
                right = nodes[m:] + todo
                return await _helper(left, right, results)
    res = await _helper(nodes, [], [])
    return res

async def create_page(title, content, author = None, author_url = None):
    html_content = clean_article_html(str(content))
    nodes = html_to_nodes(html_content)
    res = await create_page_from_nodes(title, nodes, author = author, author_url = author_url)
    return res