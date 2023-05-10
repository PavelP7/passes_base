from rest_framework import viewsets
from .serializers import *
from django.http import JsonResponse

class IncorrectFields(Exception):
    def __init__(self):
        super().__init__()

class PerevalDoesntExist(Exception):
    def __init__(self):
        super().__init__()

class PerevalViewset(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            user_data = data.pop('user')
            user = Users.objects.filter(email=user_data['email']).first()
            if not user:
                user_serializer = UsersSerializer(data=user_data)
                if user_serializer.is_valid():
                    user_serializer.save()
                    user = user_serializer.instance
                else:
                    raise IncorrectFields

            pereval_serializer = PerevalSerializer(data=data)
            if pereval_serializer.is_valid():
                pereval_serializer.save()
                pereval_id = pereval_serializer.instance.id
                UserPereval.objects.create(user=user, pereval=pereval_serializer.instance)
            else:
                raise IncorrectFields
        except IncorrectFields:
            return JsonResponse(status=400, data={"status": 400, "message": "Bad Request", "id": None})
        except:
            return JsonResponse(status=500, data={"status": 500, "message": "Ошибка подключения к базе данных", "id": None})

        return JsonResponse(status=200, data={"status": 200, "message": None, "id": pereval_id})

    def list(self, request, *args, **kwargs):
        email = request.GET['user_email']
        pereval = UserPereval.objects.filter(user__email=email).values('pereval')
        if pereval.exists():
            per = list(map(lambda pk: PerevalAdded.objects.get(pk=pk), [p['pereval'] for p in pereval]))
            response = [PerevalSerializer(p).data for p in per]
            return JsonResponse(status=200, data={"pereval": response})

        return JsonResponse(status=500, data={"status": 500, "message": "Ошибка подключения к базе данных", "id": None})

    def retrieve(self, request, pk=None):
        pereval = PerevalAdded.objects.filter(pk=pk)
        if pereval.exists():
            response = PerevalSerializer(pereval.first()).data
            return JsonResponse(status=200, data=response)

        return JsonResponse(status=500, data={"status": 500, "message": "Ошибка подключения к базе данных", "id": None})

    def patch(self, request, pk=None):
        pereval = PerevalAdded.objects.filter(pk=pk)
        data = request.data
        try:
            if pereval.exists():
                user_data = data.pop('user')
                pereval_serializer = PerevalSerializer(pereval.first(), data=data)
                if pereval_serializer.is_valid():
                    pereval_serializer.save()
                else:
                    raise IncorrectFields
            else:
                raise PerevalDoesntExist
        except IncorrectFields:
            return JsonResponse(status=400, data={"state": 0, "message": "Некорректные данные запроса"})
        except PerevalDoesntExist:
            return JsonResponse(status=400, data={"state": 0, "message": "Обновление несуществующей записи"})
        except:
            return JsonResponse(status=500, data={"state": 0, "message": "Ошибка подключения к базе данных"})

        return JsonResponse(status=200, data={"state": 1, "message": None})
