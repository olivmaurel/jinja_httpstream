StreamingHttpResponse() with templates using Jinja
==================================================


Overview
--------

This sample django project illustrates how you can use Jinja2.generate() to trick StreamingHttpResponse()
into using templates to render your http pages in a nicely formatted manner.


The problem
-----------
`As the official documentation states
<https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.StreamingHttpResponse>`_,
Django is designed for short-lived requests, and it's preferable to avoid streaming responses.
But there are cases where you have to stream data in your http response, like big csv files.
Unfortunately, as you may already know, the StreamingHttpResponse() class is not meant
to be used with a template like the normal HttpResponse() class.
So you can stream your data to the browser using a generator, and the only formatting allowed
has to go through the generator, leading to ugly and unmaintanable blobs of html (cf myapp/streaminghttpresponse view).

The solution
------------
When I stumbled upon this problem, I looked around on the web for a solution,
someone suggested the jinja2 template engine with the generate() method,
but with no indication on how to use it in Django. So I decided to write this sample project
as a guide to help others facing the same problem.

The solution in itself is pretty straightforward, and requires only to install jinja2,
and adding a few lines of codes in your views.py file::

    import os
    from jinja2 import Environment, FileSystemLoader
    from django.http import StreamingHttpResponse

    def jinja_generate_with_template(template, context):

        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        template_dir = THIS_DIR + '/templates/'
        j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

        return j2_env.get_template(template).generate(context)


You can then create a generator in your view function by calling jinja_generate_with_template(template, context)
then return it in a StreamingHttpGenerator() class, like this::

    def your_view(request):
        your_template = 'jinja2/my_awesome_template.html'
        your_context = {'foo':'bar'}
        stream = jinja_generate_with_template(your_template, your_context)
        return StreamingHttpResponse(stream)

Note: In this implementation, I had to set manually the template path (THIS_DIR), it's kinda quick and dirty and could be improved.



Setting up the sample project
-----------------------------
If you want to try the project directly, you can install it just like any other basic django projects.

Using virtualenvwrapper::

    mkvirtualenv jinja_httpstream
    workon

'jinja_httpstream' should appear in the list of existing virtual environments::

    workon jinja_httpstream

clone the repository in a dedicated directory::

    git clone https://github.com/olivmaurel/jinja_httpstream.git /path/to/my/projects

Instal the required packages::

    cd /path/to/my/projects/jinja_httpstream
    pip install -r requirements.txt

And finally run the project::

    ./manage.py runserver

Demonstration with the different urls
-------------------------------------

If you want to check the implementation live on a test page, just fire up localhost::

    ./manage.py runserver

And open the page::

    http://localhost:8000/myapp/

There are four links illustrating the limitations of HttpResponse() and StreamingHttpResponse(), and how to solve them
Just click on the links and try for yourself::

    1) Problem Rendering delay using HttpResponse() http://localhost:8000/myapp/httpresponse
    2) StreamingHttResponse() without a template http://localhost:8000/myapp/streaminghttpresponse
    3) Naive implementation of templates with StreamingHttpResponse() http://localhost:8000/myapp/naive
    4) Solution: combine StreamingHttpresponse() with jinja.generate() http://localhost:8000/myapp/jinja

Add jinja2 to an existing project
---------------------------------
If you want to use jinja2.generate() to stream and render templates in your Django project,
you can install jinja2 and with a few settings modifications you should be good to go.

If you already have jinja2 installed in your django project, just skip this part and
use directly the example described above in views.py

The solution described below comes from this article http://jonathanchu.is/posts/upgrading-jinja2-templates-django-18-with-admin/

1) Install jinja2::

    pip install jinja2

2) modify yourproject/settings.py (change 'myapp' with the name of your app)::

    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/jinja2'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'myapp.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    ]

Make sure to keep both jinja2 and django backend, since jinja2 templates may mess with the admin interface

3) Create a dedicated folder for jinja2 templates under your application main folder::

    myproject
    ├── myproject
    │   ├── __init__.py
    │   ├── jinja2.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── myapp
    │   └── views.py
    │   └── urls.py
    │   └── templates
    |        └──jinja2
    │           ├── base.html
    │           ├── home.html
    |

4) Create a jinja2.py file at the same level as your settings.py file, and paste the following code in it::

    def environment(**options):
        env = Environment(**options)
        env.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
        })
        return env

5) That's it. Now Django should be using Jinja2 template engine by default,
which is by the way a huge improvement from the default template engine.
The official Jinja2 documentation has many exemples and use cases (although not this one!) http://jinja.pocoo.org/docs/2.9/

