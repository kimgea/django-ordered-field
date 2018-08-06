=====
Usage
=====

Ordered Field
-------
The OrderedField class keeps all the records in the table in order from 0 to count - 1

.. code-block:: python

    from django_ordered_field import OrderedField


    class Table(models.Model):
        name = models.CharField(max_length=100)
        order = OrderedField()


Ordered Collection Field
-------
The OrderedCollectionField class is used to keep records in order related to another field. This can be used to make structures like ordered lists and so on.

.. code-block:: python

    from django_ordered_field import OrderedCollectionField


    class Item(models.Model):
        name = models.OrderedCollectionField(max_length=100)
        item_type = models.IntegerField()
        order = OrderedCollectionField(collection='item_type')


A collection can consist of another signle field or it can be a combination of multiple fields

.. code-block:: python

    OrderedCollectionField(collection='item_type')
    # Or
    OrderedCollectionField(collection=['list', 'sub_list'])


Update table data
-------
Inserting, updating and deletion of instances has to use methods that uses the model.save() and model.delete() methods. queryset.update(...), queryset.delete() and similar functions that omits model.save() and model.delete() will destroy the ordering of the instances.

# TODO: Concreate examples

Other fields updated when order is changed
-------
It is possible to specify other fields than the order field to be automatically updated when a field has its position changed by another field that was inserted/changed/deleted.

The update_auto_now setting will make sure that all date/datetime related fields that are taged to be automatically updated on change will be updated when the order is changed. This setting is default on, so remember to turn ot off if it is not wanted.
.. code-block:: python

    OrderedField(update_auto_now=True)


The extra_field_updates is a dictionary and it is used to specify other field to be updated when the order field is changed by anothers position change.
.. code-block:: python

    def get_loged_in_user():
        return "KGA"

    OrderedField(extra_field_updates={
                                   'order_changed_count': models.F("order_changed_count") + 1,
                                   'updated_by': get_loged_in_user
                               })

The self_updates_on_collection_change parameter is used to specify fields to be updated when an instance changes collection. Unlike the extra_field_updates which is triggered when a records osition is changed when another field has its position changed the self_updates_on_collection_change works on the active instance and only when it changes collection.
.. code-block:: python

    def get_loged_in_user():
        return "KGA"

    OrderedField(self_updates_on_collection_change={
                                   'order_changed_count': models.F("order_changed_count") + 1,
                                   'updated_by': get_loged_in_user
                               })

If self_updates_on_collection_change is the same as extra_field_updates like above then it is also possible to set the self_updates_on_collection_change_like_regular to True to avoid duplicating the settings.
.. code-block:: python

    def get_loged_in_user():
        return "KGA"

    OrderedField(self_updates_on_collection_change_like_regular=True)

Model inheritance
-------

.. code-block:: python

    class Unit(models.Model):
        name = models.CharField(max_length=100)
        position = OrderedField(parent_link_name='unittwo_ptr')


    class VideoTwo(Unit):
        description = models.CharField(max_length=100)


    add_signals(Unit, Video, "position")

Abstract model
-------

.. code-block:: python

    class CommonInfo(models.Model):
        name = models.CharField(max_length=100)
        position = OrderedField()

        class Meta:
            abstract = True


    class Person(CommonInfoTwo):
        description = models.CharField(max_length=100)

Proxy model
-------

.. code-block:: python

    class Person(models.Model):
        name = models.CharField(max_length=100)
        position = OrderedField()


    class PersonProxy(Person):

        class Meta:
            proxy = True


    add_signals_for_proxy(Person, PersonProxy, "position")


Add signals
-------
Current version has a limitation in a few circumstances than one has to mannually register some of the signals. If you use Proxy models or inherit from a model containing a order field then you have to manually register the signals.

Feel free to add a git pull request if you find a way to automatically register thise signals.
