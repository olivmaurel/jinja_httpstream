Install and run jinja-httpstream locally
========================================


Overview


Setting up
----------

Using virtualenvwrapper::

    mkvirtualenv jinja_httpstream
    workon

'jinja_httpstream' should appear in the list of existing virtual environments::

    workon jinja_httpstream

copy the repository in a dedicated directory::

    mkdir /home/username/projects/jinja_httpstream

Sync the db::

    ./manage.py syncdb

And finally run the project::

    ./manage.py runserver



Title
-----


Another title
-------------

