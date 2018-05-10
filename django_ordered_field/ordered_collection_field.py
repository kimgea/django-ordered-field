from django.db import models

from .ordered_field import OrderedField

class OrderedCollectionField(OrderedField):

    def __init__(self, verbose_name=None, name=None,
                 default=-1, collection=None, parent_link=None,
                 update_auto_now=True, *args, **kwargs):
        super(OrderedCollectionField, self).__init__(
            verbose_name=verbose_name, name=name, default=default, *args, **kwargs)

        if collection is None:
            self.collection = []
        else:
            if isinstance(collection, str):
                collection = (collection,)
            self.collection = collection

        self.parent_link = parent_link
        self._collection_changed = None

    def contribute_to_class(self, cls, name):
        super(OrderedCollectionField, self).contribute_to_class(cls, name)

    def _get_collection(self, model_instance):
        filters = {}
        if self.collection is not None:
            for field_name in self.collection:
                field = model_instance._meta.get_field(field_name)
                field_value = getattr(model_instance, field.attname)
                if field.null and field_value is None:
                    filters['%s__isnull' % field.name] = True
                else:
                    filters[field.name] = field_value
        model = type(model_instance)
        if self.parent_link is not None:
            model = model._meta.get_field(self.parent_link).rel.to
        return model._default_manager.filter(**filters)

    def get_queryset(self, model_instance):
        return self._get_collection(model_instance)


    def update_on_save(self, sender, instance, created, **kwargs):
        collection_changed = self._collection_changed
        self._collection_changed = None

        current_value, updated_value = getattr(instance, self.get_cache_name())

        if updated_value is None and not collection_changed:
            return None

        created = collection_changed or created
        super(OrderedCollectionField, self).update_on_save(
            sender, instance, created, (current_value, updated_value), **kwargs)\


    def pre_save(self, model_instance, add):
        add = self._collection_changed_then_delete_instance(model_instance, add)
        return super(OrderedCollectionField, self).pre_save(model_instance, add)

    def _has_collection_changed(self, model_instance, previous_instance, collection):
        if previous_instance is None:
            return False
        for field_name in collection:
            field = model_instance._meta.get_field(field_name)
            current_field_value = getattr(model_instance, field.attname)
            previous_field_value = getattr(previous_instance, field.attname)
            if previous_field_value != current_field_value:
                return True
        return False

    def _collection_changed_then_delete_instance(self, model_instance, add):
        if add or not self.collection:
            return add  # no need to check if new or no collection
        previous_instance = None
        try:
            previous_instance = type(model_instance)._default_manager.get(pk=model_instance.pk)
        except models.ObjectDoesNotExist:
            add = True  # New instance if no previous collection. # TODO: try to actually hit this one
        self._collection_changed = self._has_collection_changed(
            model_instance, previous_instance, self.collection)
        if self._collection_changed:
            self._remove_from_collection(previous_instance)
        return add

    def _remove_from_collection(self, model_instance):
        updates = {self.name: models.F(self.name) - 1}
        self.extra_updates_on_change(model_instance, updates)
        current = getattr(model_instance, self.get_cache_name())[0]  # magic number :(
        queryset = self._get_collection(model_instance)
        queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def _get_cleaned_current_and_updated_values(self, add, model_instance, cache_name):
        current_value, updated_value = getattr(model_instance, cache_name)

        if self._collection_changed:
            current_value = None    # Has been removed, so no current position

        return super(OrderedCollectionField, self)._get_cleaned_current_and_updated_values(
            add, model_instance, cache_name, (current_value, updated_value))
