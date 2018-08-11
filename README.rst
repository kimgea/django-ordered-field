=============================
django-ordered-field
=============================

.. image:: https://badge.fury.io/py/django-ordered-field.svg
    :target: https://badge.fury.io/py/django-ordered-field

.. image:: https://travis-ci.org/kimgea/django-ordered-field.svg?branch=master
    :target: https://travis-ci.org/kimgea/django-ordered-field

.. image:: https://codecov.io/gh/kimgea/django-ordered-field/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kimgea/django-ordered-field

A django field to make it easy to order your model instances. If you have made an ordered list and you change the position of the list item instance then all the other list iteminstances belonging to that list has their position automatically updated to keep the list ordered without holes and list items with duplicate positions.
``OrderedField field`` is a global ordering field for the entire table.
``OrderedCollectionField`` order instances with respect to one or more other fields on the instance.


Requires
--------
* python>=3.6
* django>=2.0

Documentation
-------------

The full documentation is at https://django-ordered-field.readthedocs.io.

Quickstart
----------

Install django-ordered-field::

    pip install git+https://github.com/kimgea/django-ordered-field.git


In your models.py add the field you want ``OrderedField`` or ``OrderedCollectionField``:

.. code-block:: python

    from django_ordered_field import OrderedField

    class YourModel(models.Model):
        name = models.CharField(max_length=100)
        order = OrderedField()

And your ready to go.

Features
--------

* ``OrderedField`` will keep correct ordering between all instances in the enire table
* ``OrderedCollectionField`` can seperate the table in different collection based on one or more columns and keep order in each collection
* ``update_auto_now`` will update all other fields containing auto_now=True with django.utils.timezone.now if it is set to True
* ``extra_field_updates`` can be used to update other fields when their order is changed
* ``self_updates_on_collection_change`` can be used to update self (current instance) when it changes collection. Setting ``self_updates_on_collection_change_like_regular`` to True will make it use the values from the extra_field_updates

Limitations
--------

* Must user model.save(). queryset methods does not work
* Order field cant be unique or in an uniqu_togheter constraint
* After a position has been updated, other members of the collection are updated using a single SQL UPDATE statement, this means the save method of the other instances won't be called. As a partial work-around use the ``update_auto_now``, ``extra_field_updates`` and the ``self_updates_on_collection_change`` functionalities.


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
