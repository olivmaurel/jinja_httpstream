import os
import time

from django.http import StreamingHttpResponse
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))



def simple_httpresponse(request):

    context = get_sample_context()

    return render(request, 'jinja2/content.html', context)


def get_sample_context():

    long_response = simulate_long_response_with_delay()
    mystring = 'We can pass some strings in the context, like this'
    context = {'mylist': [1, 2, 3, 4, 5], 'mystring': mystring, 'mylongresponse': long_response}

    return context


def mystreamed_content():

    template = 'jinja2/content.html'
    context = get_sample_context()

    return stream_httpresponse_with_template(template, context)


def stream_httpresponse_with_template(template, context):

    path = THIS_DIR + '/templates/'
    j2_env = Environment(loader=FileSystemLoader(path), trim_blocks=True)

    return StreamingHttpResponse(j2_env.get_template(template).generate(context))


def simulate_long_response_with_delay():

    for i in range(10):
        time.sleep(1)
        yield 'This request is taking a while... still {} seconds to go'.format(i)

