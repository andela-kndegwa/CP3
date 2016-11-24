from django.conf.urls import url, include
from api.views import BucketListViewSet, BucketListItemViewSet, UserViewSet, api_root
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers as ns_router

from rest_framework_jwt.views import obtain_jwt_token


user_register = UserViewSet.as_view({
    'post': 'create'
})

# Ensures we can nest our items in the url
# pip install drf-nested-routers for this to work
# Routers implementation allows us to configure the urls...
# without having to explicitly define the URLs manually.
router = SimpleRouter()
router.register(r'bucketlists', BucketListViewSet)

item_router = ns_router.NestedSimpleRouter(
    router, r'bucketlists', lookup='bucketlist')
item_router.register(r'items', BucketListItemViewSet)


urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^auth/register', user_register),
    url(r'^auth/login', obtain_jwt_token),
    url(r'^', include(router.urls)),
    url(r'^', include(item_router.urls)),

])

# Adds the login button to the browserify page.
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))]
