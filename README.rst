=============================
django-ordered-field
=============================

.. image:: https://badge.fury.io/py/django-ordered-field.svg
    :target: https://badge.fury.io/py/django-ordered-field

.. image:: https://travis-ci.org/kimgea/django-ordered-field.svg?branch=master
    :target: https://travis-ci.org/kimgea/django-ordered-field

.. image:: https://codecov.io/gh/kimgea/django-ordered-field/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kimgea/django-ordered-field

A django field to make it easy to order your model instances.
OrderedField field is a global ordering field for the entire table.
OrderedCollectionField order instances with respect to one or more other instance fields.

Only tested and supported for python>=3.6 and django>=2.
Check out django-positions if you need it for older versions.

Documentation
-------------

The full documentation is at https://django-ordered-field.readthedocs.io.

Quickstart
----------

Install django-ordered-field::

    pip install https://github.com/kimgea/django-ordered-field

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_ordered_field',
        ...
    )

Features
--------

* TODO

TODO
--------

* Add tests - Missing for OrderedField. And try to hit all paths
* Look for missing test for regular use cases

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Based on django-positions (it did not work for django 2):

*  django-positions_

.. _django-positions: https://github.com/jpwatts/django-positions

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
