from django.test import TestCase
from ..models import *
from .data import DATA
import base64
from django.core.files.base import ContentFile

class TestPereval(TestCase):
    @classmethod
    def setUpTestData(cls):
        coords = Coords.objects.create(latitude=DATA['coords']['latitude'], longitude=DATA['coords']['longitude'],
                                       height=DATA['coords']['height'])
        level = Levels.objects.create(winter=DATA['level']['winter'], summer=DATA['level']['summer'],
                                      autumn=DATA['level']['autumn'], spring=DATA['level']['spring'])
        pereval = PerevalAdded.objects.create(add_time=DATA['add_time'], beauty_title=DATA['beauty_title'],
                                    title=DATA['title'], other_titles=DATA['other_titles'],
                                    connect=DATA['connect'], coords=coords, level=level)
        decode = base64.b64decode(DATA['images'][0]['data'])
        data = ContentFile(decode, name=DATA['images'][0]['title'])
        Image.objects.create(data=data, title=DATA['images'][0]['title'], pereval=pereval)

    def test_choises_pereval_status(self):
        pereval = PerevalAdded.objects.get(pk=1)
        status = pereval.get_status_display()
        self.assertEqual(status, 'new')
        pereval.status = PerevalAdded.PENDING
        pereval.save()
        status = pereval.get_status_display()
        self.assertEqual(status, 'pending')
        pereval.status = PerevalAdded.ACCEPTED
        pereval.save()
        status = pereval.get_status_display()
        self.assertEqual(status, 'accepted')
        pereval.status = PerevalAdded.REJECTED
        pereval.save()
        status = pereval.get_status_display()
        self.assertEqual(status, 'rejected')

    def test_uploading_image_path(self):
        image = Image.objects.get(pk=1)
        self.assertIn(f"images\\{image.pereval.title}\\{image.title}", image.data.path)


