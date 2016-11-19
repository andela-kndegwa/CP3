from django.conf.urls import url
from api.views import BucketListViewSet, api_root
from rest_framework import format_suffix_patterns


bucketlist = BucketListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^bucketlists/$', bucketlist, name='bucketlists'),
])
