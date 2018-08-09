from django.db import models
from .ordered_field import (OrderedField)
from django_ordered_field.common import (extra_updates)


class OrderedCollectionField(OrderedField):

    description = "Position in an ordered collection"

    def __init__(self, collection, verbose_name=None, name=None,
                 default=-1, update_auto_now=True, extra_field_updates=None,
                 self_updates_on_collection_change=None,
                 self_updates_on_collection_change_like_regular=False,
                 *args, **kwargs):
        super(OrderedCollectionField, self).__init__(
            verbose_name=verbose_name, name=name, default=default,
            update_auto_now=update_auto_now, extra_field_updates=extra_field_updates,
            *args, **kwargs)
        if collection is None or not collection:
            raise TypeError(
                "{0} must have a collection, else use ordered_field".
                format(self.__class__.__name__))
        self.collection = (collection,) if isinstance(collection, str) else collection
        self._collection_changed = None
        self.self_updates_on_collection_change = extra_field_updates \
            if self_updates_on_collection_change_like_regular else {}
        if self_updates_on_collection_change is not None:
            self.self_updates_on_collection_change = self_updates_on_collection_change

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["collection"] = self.collection
        if self.self_updates_on_collection_change is not None:
            kwargs["self_updates_on_collection_change"] = self.self_updates_on_collection_change
        return name, path, args, kwargs

    def get_queryset(self, model_instance):
        return self.get_collection(model_instance)

    def get_collection(self, model_instance):
        filters = {}
        for field_name in self.collection:
            field = model_instance._meta.get_field(field_name)
            field_value = getattr(model_instance, field.attname)
            if field.null and field_value is None:
                filters['%s__isnull' % field.name] = True  # Collection item is null
            else:
                filters[field.name] = field_value
        return self.get_model(model_instance)._default_manager.filter(**filters)

    def post_save_handler(self, sender, instance, created, **kwargs):
        collection_changed = self._collection_changed
        self._collection_changed = None
        current_value, updated_value = getattr(instance, self.get_cache_name())
        if current_value == updated_value and not collection_changed:
            return None  # No positional changes, no need to update
        created = collection_changed or created
        super(OrderedCollectionField, self).post_save_handler(
            sender, instance, created, (current_value, updated_value), **kwargs)

    def pre_save_handler(self, sender, instance, **kwargs):
        self.collection_changed_then_delete_instance(instance)
        super(OrderedCollectionField, self).pre_save_handler(
            sender, instance, updates=self.get_self_updates_if_collection_changed(),
            **kwargs)

    def get_self_updates_if_collection_changed(self):
        if not self._collection_changed:
            return None
        updates = {}
        extra_updates(updates, self.self_updates_on_collection_change)
        return updates

    def collection_changed_then_delete_instance(self, model_instance):
        try:
            previous_instance = type(model_instance)._default_manager.get(pk=model_instance.pk)
        except models.ObjectDoesNotExist:
            return
        self._collection_changed = self.has_collection_changed(
            model_instance, previous_instance)
        if self._collection_changed:
            self.remove_from_collection(previous_instance)

    def has_collection_changed(self, current_instance, previous_instance):
        for field_name in self.collection:
            field = current_instance._meta.get_field(field_name)
            current_field_value = getattr(current_instance, field.attname)
            previous_field_value = getattr(previous_instance, field.attname)
            if previous_field_value != current_field_value:
                return True
        return False

    def remove_from_collection(self, model_instance):
        updates = {self.name: models.F(self.name) - 1}
        self.extra_updates_on_change(model_instance, updates)
        current = getattr(model_instance, self.get_cache_name())[0]  # magic number :(
        queryset = self.get_queryset(model_instance)
        queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def get_cleaned_current_and_updated_values(self, add, model_instance, cache_name, values=None):
        current_value, updated_value = getattr(model_instance, cache_name)
        if self._collection_changed:
            if updated_value is None:
                # item changing position will be placed in current position if a new was not given
                updated_value = current_value
            current_value = None    # Has been removed from collection, so no current position
        return super(OrderedCollectionField, self).get_cleaned_current_and_updated_values(
            add, model_instance, cache_name, (current_value, updated_value))
