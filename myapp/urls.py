from django.conf.urls import url

from myapp import views

urlpatterns = [
    url(r'^simple_httpresponse$', views.simple_httpresponse, name='simple_httpresponse'),
    url(r'^mystreamed_content$', views.mystreamed_content, name='mystreamed_content$'),
]