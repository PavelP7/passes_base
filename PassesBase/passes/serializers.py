from .models import *
from rest_framework import serializers

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
    class Meta:
        model = Image
        fields = ['title']

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
            Image.objects.create(pereval=pereval, **image_data)

        return pereval
