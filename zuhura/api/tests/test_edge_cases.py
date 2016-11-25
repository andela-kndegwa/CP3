from rest_framework import status

from utils import (BaseEndPoint,
                   make_get_request,
                   make_put_request,
                   make_post_request,
                   make_delete_request)
from faker import Faker

fake = Faker()


class TestEdgeCasesForEndPoints(BaseEndPoint):
    def test_cannot_access_someone_elses_bucketlist(self):
        user_2 = {}
        user_2['username'] = fake.user_name()
        user_2['email'] = fake.email()
        user_2['password'] = fake.password()
        # register user
        make_post_request(url=self.signup_url,
                          client=self.client,
                          data=user_2)
        # log in user
        login_data = {
            'username': user_2['username'],
            'password': user_2['password']
        }
        login = make_post_request(url=self.login_url,
                                  client=self.client,
                                  data=login_data)

        token = str(login.data['token'])
        # client credentials
        # Set up and ensure token
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # Allow this user to access the bucket list in set up
        rv = make_get_request(url=self.bucketlists_url +
                              '1/', client=self.client)
        # Try to access the protected bucket list should return a Forbidden
        # error.
        self.assertEquals(rv.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(rv.data['detail'],
                          'You do not have permission to perform this action.')

    def test_cannot_create_a_bucket_list_without_name(self):
        data = {
            "name": ''
        }
        rv = make_post_request(
            client=self.client, url=self.bucketlists_url, data=data)
        self.assertEqual(rv.data['name'][0], 'This field may not be blank.')

    def test_cannot_create_an_item_without_name(self):
        item_data = {
            "name": ""
        }
        rv = make_post_request(
            client=self.client, url=self.bucketlists_url + '1/items/', data=item_data)
        self.assertEqual(rv.data['name'][0], 'This field may not be blank.')

    def test_access_bucketlist_that_does_not_exist(self):
        rv = make_get_request(client=self.client,
                              url=self.bucketlists_url + 'abcdef/')
        self.assertEqual(rv.status_text, 'Not Found')
        self.assertEqual(rv.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_exist_item_that_does_not_exist(self):
        rv = make_get_request(client=self.client,
                              url=self.bucketlists_url + '1/items/1004/')
        self.assertEqual(rv.status_text, 'Not Found')
        self.assertEqual(rv.status_code, status.HTTP_404_NOT_FOUND)
