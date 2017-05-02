from django.conf.urls import url

from myapp import views

urlpatterns = [
    url(r'^$', views.index, name='httpresponse'),
    url(r'^httpresponse$', views.simple_httpresponse, name='httpresponse'),
    url(r'^streaminghttpresponse$', views.simple_streaminghttpresponse, name='streaminghttpresponse$'),
    url(r'^jinja$', views.streaminghttpresponse_with_jinja, name='streaming_with_jinja$'),
    url(r'^naive$', views.naive_template_implementation_with_streaminghttpresponse, name='test$'),
]