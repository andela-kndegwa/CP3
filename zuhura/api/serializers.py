from django.db import IntegrityError

from rest_framework import serializers
from api.models import BucketList, BucketListItem
from django.contrib.auth.models import User

from django.utils.timezone import now


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=None,
        min_length=None,
        allow_blank=False),

    email = serializers.EmailField(
        max_length=None,
        min_length=None,
        allow_blank=False)

    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password'},
        required=True,
        write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")


class BucketListItemSerializer(serializers.ModelSerializer):
    bucketlist = serializers.PrimaryKeyRelatedField(read_only=True)
    is_done = serializers.BooleanField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    # set a unique on the model field
    # set an error on the serializer and catch the particular error

    def create(self, validated_data):
        try:
            if not validated_data.get("name"):
                raise serializers.ValidationError(
                    "Bucket list name cannot be empty")
            return super(BucketListItemSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'That bucket list item name already exists.')

    def update(self, instance, validated_data):
        instance.date_modified = now()
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        try:
            return super(BucketListItemSerializer, self).update(instance,
                                                                validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'That bucket list item name already exists.')

    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'is_done', 'created_on',
                  'modified_on', 'description', 'bucketlist')


class BucketListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='bucketlist-detail',
                                               format='html')
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    items = BucketListItemSerializer(many=True, read_only=True)

    created_on = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False,
        read_only=True)

    modified_on = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False)

    class Meta:
        model = BucketList
        fields = ("id", "owner", "name", "description",
                  "items", "created_on", "modified_on", "url")

    def create(self, validated_data):
        try:
            if not validated_data.get("name"):
                raise serializers.ValidationError(
                    "Bucket list name cannot be empty")
            return super(BucketListSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'That bucket list name already exists.')

    def update(self, instance, validated_data):
        instance.date_modified = now()
        try:
            return super(BucketListSerializer, self).update(instance,
                                                            validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'That bucket list name already exists.')
