from utils import (make_post_request,
                   BaseEndPoint,
                   make_get_request,
                   make_put_request,
                   make_delete_request)
from rest_framework import status

from api.models import BucketList


class TestBucketListEndPoint(BaseEndPoint):
    # Test Create Bucket List functionality.
    def test_creates_bucketlist(self):
        '''
        Method:
            POST
        Asserts:
            Asserts one can create a bucket list.

        '''
        self.assertEqual(self.bucket_response.status_code,
                         status.HTTP_201_CREATED)
        bucketlist_count_after = BucketList.objects.all().count()
        self.assertEqual(bucketlist_count_after - self.bucketlists_before, 1)

    def test_retrieves_created_bucketlist(self):
        '''
        Method:
            GET
        Asserts:
            Asserts one can get a created bucket list.

        '''
        response = make_get_request(
            client=self.client, url=self.bucketlists_url + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Stay Foolish', response.data['description'])
    # Test Put Bucket List Functionality

    def test_updates_bucketlist(self):
        '''
        Method:
            PUT
        Asserts:
            Asserts one can updated a created bucket list.

        '''
        data = {
            'name': 'Changed Name'
        }
        response = make_put_request(client=self.client,
                                    url=self.bucketlists_url + '1/',
                                    data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Changed Name')

    def test_delete_bucketlist(self):
        '''
        Method:
            DELETE
        Asserts:
            Asserts one can delete a created bucket list.

        '''
        response = make_delete_request(
            client=self.client, url=self.bucketlists_url + '1/')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)


class TestBucketListItemEndPoint(BaseEndPoint):

    def test_creates_item(self):
        '''
        Method:
            POST
        Asserts:
            Asserts one can create a bucket list item.

        '''
        data = {
            "name": "Bucket List Item Sample two",
        }
        response = make_post_request(
            client=self.client, url=self.bucketlists_url + '1/items/',
            data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Bucket List Item Sample two")

    def test_updates_item_functionality(self):
        '''
        Method:
            UPDATE
        Asserts:
            Asserts one can update a created bucket list item.

        '''
        data = {
            "is_done": True
        }
        response = make_put_request(
            client=self.client,
            url=self.bucketlists_url + '1/items/1/',
            data=data)
        self.assertEqual(response.data['is_done'], True)

    def test_deletes_item_functionality(self):
        '''
        Method:
            DELETE
        Asserts:
            Asserts one can delete a created bucket list item.

        '''
        response = make_delete_request(client=self.client,
                                       url=self.bucketlists_url + '1/items/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
