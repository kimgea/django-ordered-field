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


Requires
--------
* python>=3.6
* django>=2.

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

In your models.py add the field you want ``OrderedField`` or ``OrderedCollectionField``:

.. code-block:: python

    from django_ordered_field import OrderedField

    class YourModel(models.Model):
        name = models.CharField(max_length=100)
        order = OrderedField()

And your ready to go.

Features
--------


TODO
--------

* Add tests - Missing for OrderedField. And try to hit all paths
* Look for missing test for regular use cases
* Make example project

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ python setup.py test



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
