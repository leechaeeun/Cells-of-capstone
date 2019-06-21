from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^result', views.result, name='result'),
    url(r'^cellsofcapstone', views.cellsofcapstone_main, name='cellsofcapstone'),
    url(r'^adddiagnosis', views.add_diagnosis, name='adddiagnosis'),
    url(r'^addmedication', views.add_medication, name='addmedication'),
    url(r'^completediagnosis', views.complete_diagnosis, name='completediagnosis'),
    url(r'^completemedication', views.complete_medication, name='completemedication'),
]
