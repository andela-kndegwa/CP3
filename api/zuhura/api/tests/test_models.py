from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase

from factories import (UserModelFactory,
                       BucketListFactory, BucketListItemFactory)


class TestDuplicateUserNameCannotBeCreated(TransactionTestCase):
    '''
    TransactionTestCase bypasses the error throwing checks as made to
    the database through a process known as table truncation thus great
    for evaluating an IntegrityError.
    '''

    def test_cannot_create_duplicate_users(self):
        user = User.objects.create(username='eli', password='pass123')
        user.save()
        with self.assertRaises(IntegrityError):
            user = User.objects.create(username='eli', password='pass')


class BaseTestCase(TestCase):
    '''
    Purpose:
    Abstract the repeated use of the Test Classes and allows for
    single instantiation of objects.

    Instantiates:
           UserModelFactory
           BucketListFactory
           BucketListItemFactory
    '''
    def setUp(self):
        self.user = UserModelFactory()
        self.second_user = UserModelFactory(username='Amina')
        self.bucketlist = BucketListFactory()
        self.item = BucketListItemFactory()


class TestUserModelFunctionality(BaseTestCase):
    '''
    Inherits:
            BaseTestCase
    '''
    def test_user_model_functionality(self):
        self.assertEquals(self.user.username, 'jamleck')
        self.assertEquals(self.second_user.username, 'Amina')


class TestBucketListFunctionality(BaseTestCase):
    '''
    Inherits:
            BaseTestCase
    '''
    def test_bucket_list_name(self):
        self.assertEquals(self.bucketlist.name, 'Things to do 2017')

    def test_owner_of_the_created_bucketlist(self):
        # This test ensures that the bucket list owner is indeed jamleck
        # The str() type casting ensures that the result is first converted
        # from Unicode to a string as with Python 2.7
        self.assertEqual(str(self.bucketlist.owner), 'jamleck')


class TestItemFuctionality(BaseTestCase):
    '''
    Inherits:
            BaseTestCase
    '''
    def test_assert_bucket_list_item_name(self):
        self.assertEqual(self.item.name, 'Travel to Canada')

    def test_item_is_instantiated_with_a_false_status(self):
        # On creation a bucket list item is instantiated as not done by
        # default.
        self.assertFalse(self.item.is_done)

    def test_item_belongs_to_a_bucketlist(self):
        # A bucket list item is associated with a particular
        # bucket list thus the proof.
        self.assertEqual(self.item.bucketlist.name, 'Things to do 2017')

    def test_item_belongs_to_same_owner(self):
        # The item belongs to a bucket list which belongs to
        # someone.
        # Conversion to Unicode is still important due to use of
        # Python 2.7 for the set up.
        self.assertEquals(str(self.item.bucketlist.owner), 'jamleck')
