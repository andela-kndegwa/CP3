from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from faker import Faker

from utils import make_post_request, make_get_request
from test_registeration import TestUserRegisteration


class TestUserAuthentication(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake_credentials = Faker()
        self.login_url = '/api/v1.0/auth/login'
        self.user_1 = {}
        self.user_1['username'] = str(self.fake_credentials.user_name())
        self.user_1['email'] = str(self.fake_credentials.email())
        self.user_1['password'] = str(self.fake_credentials.password())

        # Register a User with the Zuhura API
        self.login_response = make_post_request(client=self.client,
                                                url=self.login_url,
                                                data=self.user_1)

    def test_assert_client_credentials_are_non_existent(self):
        '''
        Arguments:
            client.credentials() is used by the Django Client to provide the
            necessary credentials as with the Token created after login.

        Asserts:
            The client.credentials() should be None as a token has not been
            provided.
        '''
        self.assertIsNone(self.client.credentials())

    def test_cannot_access_bucketlists_before_successful_login(self):
        '''
        Arguments:
            URL - The bucket lists URL for the Zuhura API.

        Asserts:
            GET is not successful since the resource is protected.
        '''
        bucketlist_url = '/api/v1.0/bucketlists/'
        response = make_get_request(client=self.client, url=bucketlist_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_username_required_for_login(self):
        '''
        Arguments:
            URL - The login URL for the Zuhura API.

        Asserts:
            400 Bad Request since the username is missing.
        '''
        del self.user_1['username']
        response = make_post_request(client=self.client,
                                     url=self.login_url, data=self.user_1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['username'][
                          0], 'This field is required.')

    def test_password_required_for_login(self):
        '''
        Arguments:
            URL - The login URL for the Zuhura API.

        Asserts:
            400 Bad Request since the password missing.
        '''
        del self.user_1['password']
        response = make_post_request(client=self.client,
                                     url=self.login_url, data=self.user_1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['password'][
                          0], 'This field is required.')

    def test_username_and_password_cannot_be_blank(self):
        '''
        Arguments:
            URL - The login URL for the Zuhura API.
            DATA - blank user name or blank password

        Asserts:
            400 Bad Request since either cannot be blank
        '''
        # Testing a blank user name
        self.user_1['username'] = ''
        response = make_post_request(client=self.client,
                                     url=self.login_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['username'][0],
                          'This field may not be blank.')
        # Testing a blank password
        self.user_1['password'] = ''
        response = make_post_request(client=self.client,
                                     url=self.login_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['password'][0],
                          'This field may not be blank.')

    def test_username_and_password_grants_token(self):
        '''
        Arguments:
            REGISTERATION_URL - The registration url for the Zuhura API
            LOGIN URL - The login URL for the Zuhura API.
            DATA - blank user name or blank password

        Asserts:
            201 created since the requests is a post request.

        Returns:
            Token
        '''
        # Register a user
        registration_url = '/api/v1.0/auth/register'
        make_post_request(client=self.client,
                          url=registration_url, data=self.user_1)
        # Login a user
        data = {
            "username": self.user_1['username'],
            "password": self.user_1['password']
        }
        response = make_post_request(
            client=self.client, url=self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
