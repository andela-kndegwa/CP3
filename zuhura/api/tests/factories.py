from datetime import datetime
from factory import Factory, SubFactory

from django.contrib.auth.models import User
from api.models import BucketList, BucketListItem


class UserModelFactory(Factory):

    class Meta:
        model = User

    username = 'jamleck'
    password = 'ndegwa'
    email = 'jamleck@ndegwa.com'


class BucketListFactory(Factory):

    class Meta:
        model = BucketList

    name = 'Things to do 2017'
    created_on = datetime.now()
    modified_on = datetime.now()
    owner = SubFactory(UserModelFactory)


class BucketListItemFactory(Factory):
    class Meta:
        model = BucketListItem

    bucketlist = SubFactory(BucketListFactory)
    name = 'Travel to Canada'
    is_done = False
    created_on = datetime.now()
    modified_on = datetime.now()
