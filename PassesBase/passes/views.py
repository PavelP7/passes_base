from rest_framework import viewsets
from .serializers import *
from django.http import JsonResponse

class MissedFields(Exception):
    def __init__(self):
        super().__init__()

class PerevalViewset(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            user_data = data.pop('user')
            user_serializer = UsersSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise MissedFields

            pereval_serializer = PerevalSerializer(data=data)
            if pereval_serializer.is_valid():
                pereval_serializer.save()
                pereval_id = pereval_serializer.instance.id
            else:
                raise MissedFields
        except MissedFields:
            return JsonResponse({"status": 400, "message": "Bad Request", "id": None})
        except:
            return JsonResponse({"status": 500, "message": "Ошибка подключения к базе данных", "id": None})

        return JsonResponse({"status": 200, "message": None, "id": pereval_id})
