from django.test import TestCase
from ..views import *
from .data import DATA

class TestPereval(TestCase):
    class Request:
        def __init__(self, **kwargs):
            self.data = DATA.copy()
            for k, v in kwargs.items():
                self.data[k] = v
            self.GET = {'user_email': self.data['user']['email']}

    @classmethod
    def setUpTestData(cls):
        pass

    def test_rest_api(self):
        request = self.Request(title='Тест1')
        response = PerevalViewset.create(PerevalViewset, request)
        self.assertEqual(response.status_code, 200, "Pereval creating isn't correct")
        pereval_id = PerevalAdded.objects.filter(title=request.data['title']).first().pk
        response = PerevalViewset.retrieve(PerevalViewset, None, pk=pereval_id)
        self.assertEqual(response.status_code, 200, "Pereval getting by ID isn't correct")
        response = PerevalViewset.list(PerevalViewset, request)
        self.assertEqual(response.status_code, 200, "Pereval getting by EMAIL isn't correct")
        request = self.Request(title='Тест1-обновление')
        response = PerevalViewset.patch(PerevalViewset, request, pk=pereval_id)
        self.assertEqual(response.status_code, 200, "Pereval updating isn't correct")
        title = PerevalAdded.objects.get(pk=pereval_id).title
        self.assertEqual(request.data['title'], title, "Pereval updating isn't correct")

    def test_error_creating_pereval(self):
        request = self.Request(title=None)
        response = PerevalViewset.create(PerevalViewset, request)
        self.assertEqual(response.status_code, 400, "Pereval creating error isn't correct")
        request = self.Request(title='Тест2')
        request.data.pop('user')
        response = PerevalViewset.create(PerevalViewset, request)
        self.assertEqual(response.status_code, 500, "Pereval creating error isn't correct")

    def test_error_getting_pereval(self):
        request = self.Request()
        request.data['user']['email'] = 'qwertyNotExist@mail.ru'
        response = PerevalViewset.retrieve(PerevalViewset, None, pk=100)
        self.assertEqual(response.status_code, 500, "Pereval getting by ID error isn't correct")
        response = PerevalViewset.list(PerevalViewset, request)
        self.assertEqual(response.status_code, 500, "Pereval getting by EMAIL error isn't correct")

    def test_error_updating_pereval(self):
        request = self.Request(title='Тест4')
        response = PerevalViewset.create(PerevalViewset, request)
        pereval_id = PerevalAdded.objects.filter(title=request.data['title']).first().pk
        self.assertEqual(response.status_code, 200, "Pereval creating isn't correct")
        request = self.Request(title='Тест4-обновление')
        response = PerevalViewset.patch(PerevalViewset, request, pk=100)
        self.assertEqual(response.status_code, 400, "Pereval updating by ID error isn't correct")
        request = self.Request(title=None)
        response = PerevalViewset.patch(PerevalViewset, request, pk=pereval_id)
        self.assertEqual(response.status_code, 400, "Pereval updating error isn't correct")
        request = self.Request(title='Тест4')
        request.data.pop('user')
        response = PerevalViewset.patch(PerevalViewset, request, pk=pereval_id)
        self.assertEqual(response.status_code, 500, "Pereval updating error isn't correct")
