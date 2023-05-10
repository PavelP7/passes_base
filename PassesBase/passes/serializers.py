from .models import *
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from PassesBase.settings import SITE_URL

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['winter', 'summer', 'autumn', 'spring']

class ImageSerializer(serializers.ModelSerializer):
    data = serializers.CharField(max_length=None)

    class Meta:
        model = Image
        fields = ['title', 'data']

    def to_representation(self, instance):
        self.fields.pop('data')
        data = super(ImageSerializer, self).to_representation(instance)
        data['data'] = SITE_URL[:-1] + Image.objects.get(pk=instance.pk).data.url

        return data

class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)
    level = LevelsSerializer()

    class Meta:
        model = PerevalAdded
        fields = ['add_time', 'beauty_title', 'title', 'other_titles',
                  'connect', 'coords', 'level', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')

        coords = Coords.objects.create(**coords_data)
        level = Levels.objects.create(**level_data)
        pereval = PerevalAdded.objects.create(coords=coords, level=level, **validated_data)
        for image_data in images_data:
            img = image_data['data']
            title = image_data['title']
            decode = base64.b64decode(img)
            data = ContentFile(decode, name=title)
            Image.objects.create(pereval=pereval, data=data, title=title)

        return pereval

    def to_representation(self, instance):
        self.fields.pop('images')
        data = super(PerevalSerializer, self).to_representation(instance)
        queryset = Image.objects.filter(pereval__pk=instance.pk)
        data['images'] = ImageSerializer(queryset, many=True).data
        data['status'] = PerevalAdded.objects.filter(pk=instance.pk).first().get_status_display()

        return data

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')

        instance.level.winter = level_data.get("winter", instance.level.winter)
        instance.level.summer = level_data.get("summer", instance.level.summer)
        instance.level.autumn = level_data.get("autumn", instance.level.autumn)
        instance.level.spring = level_data.get("spring", instance.level.spring)
        instance.level.save()

        instance.coords.latitude = coords_data.get("latitude", instance.coords.latitude)
        instance.coords.longitude = coords_data.get("longitude", instance.coords.longitude)
        instance.coords.height = coords_data.get("height", instance.coords.height)
        instance.coords.save()

        instance.add_time = validated_data.get("add_time", instance.add_time)
        instance.beauty_title = validated_data.get("beauty_title", instance.beauty_title)
        instance.title = validated_data.get("title", instance.title)
        instance.other_titles = validated_data.get("other_titles", instance.other_titles)
        instance.connect = validated_data.get("connect", instance.connect)
        instance.save()

        for instance_image in Image.objects.filter(pereval=instance):
            image_data = images_data.pop(0)
            instance_image.title = image_data.get("title", instance_image.title)
            decode = base64.b64decode(image_data.get("data"))
            instance_image.data = ContentFile(decode, name=instance_image.title)
            instance_image.save()

        return instance
