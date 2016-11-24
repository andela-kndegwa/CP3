from utils import make_post_request, BaseEndPoint, make_get_request, make_put_request
from rest_framework import status

from api.models import BucketList


class TestBucketListEndPoint(BaseEndPoint):
    # Test Create Bucket List functionality.
    def test_returns_empty_list_if_no_bucketlists_present(self):
        response = make_get_request(
            client=self.client, url=self.bucketlists_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creates_bucketlist(self):
        self.assertEqual(self.bucket_response.status_code,
                         status.HTTP_201_CREATED)
        bucketlist_count_after = BucketList.objects.all().count()
        self.assertEqual(bucketlist_count_after - self.bucketlists_before, 1)

    def test_retrieves_created_bucketlist(self):
        response = make_get_request(
            client=self.client, url=self.bucketlists_url + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Stay Foolish', response.data['description'])
    # Test Put Bucket List Functionality

    def test_updates_bucketlist(self):
        data = {
            'name': 'Changed Name'
        }
        response = make_put_request(client=self.client,
                                    url=self.bucketlists_url + '1/',
                                    data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Changed Name')
