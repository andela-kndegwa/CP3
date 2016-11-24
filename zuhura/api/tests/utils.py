from rest_framework.test import APITestCase, APIClient
from faker import Faker

from api.models import BucketList
from factories import BucketListFactory


def make_post_request(client, url, data, format='json'):
    response = client.post(url, data, format='json')
    return response


def make_get_request(client, url):
    response = client.get(url)
    return response


def make_put_request(client, url, data, format='json'):
    response = client.put(url, data, format='json')
    return response


class BaseEndPoint(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake_credentials = Faker()
        self.signup_url = '/api/v1.0/auth/register'
        self.login_url = '/api/v1.0/auth/login'
        self.bucketlists_url = '/api/v1.0/bucketlists/'
        self.user_1 = {}
        self.user_1['username'] = str(self.fake_credentials.user_name())
        self.user_1['email'] = str(self.fake_credentials.email())
        self.user_1['password'] = str(self.fake_credentials.password())
        # register User
        make_post_request(client=self.client,
                          url=self.signup_url,
                          data=self.user_1
                          )
        # login user
        data = {
            "username": self.user_1['username'],
            "password": self.user_1['password']
        }
        self.response = make_post_request(client=self.client,
                                          url=self.login_url,
                                          data=data)
        self.token = str(self.response.data['token'])
        # client credentials
        # Set up and ensure token
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        # bucket list count before
        self.bucketlists_before = BucketList.objects.all().count()
        self.bucketlist = BucketListFactory()
        data = {
            'name': self.bucketlist.name,
            'description': self.bucketlist.description
        }
        self.bucket_response = make_post_request(client=self.client,
                                                 url=self.bucketlists_url, data=data)
