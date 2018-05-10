=============================
django-ordered-field
=============================

.. image:: https://badge.fury.io/py/django-ordered-field.svg
    :target: https://badge.fury.io/py/django-ordered-field

.. image:: https://travis-ci.org/kimgea/django-ordered-field.svg?branch=master
    :target: https://travis-ci.org/kimgea/django-ordered-field

.. image:: https://codecov.io/gh/kimgea/django-ordered-field/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kimgea/django-ordered-field

Django field arange  model instances in an ordered fashion

Documentation
-------------

The full documentation is at https://django-ordered-field.readthedocs.io.

Quickstart
----------

Install django-ordered-field::

    pip install django-ordered-field

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_ordered_field.apps.DjangoOrderedFieldConfig',
        ...
    )

Add django-ordered-field's URL patterns:

.. code-block:: python

    from django_ordered_field import urls as django_ordered_field_urls


    urlpatterns = [
        ...
        url(r'^', include(django_ordered_field_urls)),
        ...
    ]

Features
--------

* TODO

TODO
--------

* Add tests - missing for some detail.collection functions
* Look for missing test for regular use cases
* Look for a way to easily query for last element
* Look for easy ways to move to last position

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
