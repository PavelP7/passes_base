from rest_framework import routers
from .views import PerevalViewset
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'passes', PerevalViewset, 'passes-all')

urlpatterns = [
   path('', include(router.urls)),
]
