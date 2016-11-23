def make_post_request(client, url, data, format='json'):
    response = client.post(url, data, format='json')
    return response
