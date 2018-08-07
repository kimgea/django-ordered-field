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


In your models.py add the field you want ``OrderedField`` or ``OrderedCollectionField``:

.. code-block:: python

    from django_ordered_field import OrderedField

    class YourModel(models.Model):
        name = models.CharField(max_length=100)
        order = OrderedField()

And your ready to go.

Features
--------

* OrderedField will keep correct ordering between all instances in the enire table
* OrderedCollectionField can seperate the table in different collection based on one or more columns and keep order in each collection
* update_auto_now will update all other fields containing auto_now=True with django.utils.timezone.now if it is set to True
* extra_field_updates can be used to update other fields when their order is changed

Limitations
--------

* Must user model.save(). queryset methods does not work
* Order field cant be unique or in an uniqu_togheter constraint

Not in readme, but move to doc

* Regular inheritance does not work when updating position by using parent class (works with parent_link). Other classes inheriting from it is also changed, and wrongly


TODO
--------

* Add documentation
* Collection change update parameter... look for a better name
* naming of instance variables might be confusing, look at it.
* Same for naming of add_signals. Make custom named function for each use case
* Look for more refactoring
* Finish setup.py
* Check requirements.txt
* Cleanup readme
* Check project files
* Register on pip
* Register on django
* Make example project - eh, probably skiping it


Credits
-------

Based on django-positions (it did not work for django 2 at the time):

*  django-positions_

.. _django-positions: https://github.com/jpwatts/django-positions

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
