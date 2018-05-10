=====
Usage
=====

To use django-ordered-field in a project, add it to your `INSTALLED_APPS`:

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
