def make_post_request(client, url, data, format='json'):
    response = client.post(url, data, format='json')
    return response
def make_get_request(client, url):
    response = client.get(url)
    return response