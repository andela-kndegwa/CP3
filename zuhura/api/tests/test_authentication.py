from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from faker import Faker

from utils import make_post_request


class TestUserAuthentication(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake_credentials = Faker()
        self.registeration_url = '/api/v1.0/auth/register'
        self.user_1 = {}
        self.user_1['username'] = str(self.fake_credentials.user_name())
        self.user_1['email'] = str(self.fake_credentials.email())
        self.user_1['password'] = str(self.fake_credentials.password())

        # Register a User with the Zuhura API
        self.signup_response = make_post_request(client=self.client,
                                                 url=self.registeration_url,
                                                 data=self.user_1)

    def test_usernam_required_for_registeration(self):
        '''
        Arguments:
            Drops the 'user name' in the self.data
            passed to the post request.

        Returns:
            400 i.e Bad Request

        Asserts:
            user name is required in the json data posted to the client.

        '''
        del self.user_1['username']
        response = make_post_request(client=self.client,
                                     url=self.registeration_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['username'][0],
                          'This field is required.')
        # Test User name may not be blank
        self.user_1['username'] = ''
        response = make_post_request(client=self.client,
                                     url=self.registeration_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['username'][0],
                          'This field may not be blank.')

    def test_email_required_for_registeration(self):
        '''
        Arguments:
            Drops the 'email' in the self.data
            passed to the post request.

        Returns:
            400 i.e Bad Request

        Asserts:
            email key is required in the json data posted to the client.

        '''
        del self.user_1['email']
        self.user_1['username'] = self.fake_credentials.user_name()
        response = make_post_request(client=self.client,
                                     url=self.registeration_url,
                                     data=self.user_1)
        self
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['email'][0], 'This field is required.')
        # Test email may not be blank
        self.user_1['email'] = ''
        response = make_post_request(client=self.client,
                                     url=self.registeration_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['email'][0],
                          'This field may not be blank.')

    def test_duplicate_usernames_are_not_allowed(self):
        '''
        Arguments:
            user name, email and password exactly the same
            as the one posted in the set up class

        Returns:
            400 i.e Bad Request

        Asserts:
            Duplicate users cannot be created.

        '''
        response = make_post_request(client=self.client,
                                     url=self.registeration_url,
                                     data=self.user_1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['username'][0],
                          'A user with that username already exists.')

    def test_user_registeration(self):
        self.assertEquals(
            self.signup_response.status_code,
            status.HTTP_201_CREATED)
        self.assertEquals(
            self.signup_response.status_text, 'Created')
