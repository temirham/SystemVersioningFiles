from rest_framework import serializers
from Soft_Loading.models import *
from Soft_Site.settings import MEDIA_ROOT


class SubCategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='sub_cat_id')
    # main_cat = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class MainCategoriesSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoriesSerializer(many=True, read_only=True)
    id = serializers.IntegerField(source='main_cat_id')

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'sub_categories']


class PlatformsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='platform_id')

    class Meta:
        model = Platform
        fields = ['id', 'name']


class FilesSerializer(serializers.ModelSerializer):
    platform = PlatformsSerializer(source='platform_id', read_only=True)
    id = serializers.IntegerField(source='file_id')

    class Meta:
        model = File
        fields = ['id', 'size', 'architecture', 'version',
                  'compatibility', 'languages', 'creator', 'soft_id',
                  'platform_id', 'platform']


class SoftSimpleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='soft_id')
    class Meta:
        model = Soft
        fields = ['id', 'name', 'is_primary', 'image']


class SoftSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="soft_id")
    files = FilesSerializer(many=True, read_only=True)

    class Meta:
        model = Soft
        fields = ["id", "name", "description", "is_primary",'main_cat_id', "image",
                  "files"]


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="subscr_id")

    class Meta:
        model = Soft
        fields = ["id", "user_uid", "is_active", "is_paid", "start_date",
                  "end_date", 'pay_date', 'status']