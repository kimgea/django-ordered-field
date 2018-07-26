from django.db import models
from .ordered_field import OrderedField


class OrderedCollectionField(OrderedField):

    description = "Position in an ordered collection"

    def __init__(self, collection, verbose_name=None, name=None,
                 default=-1,
                 update_auto_now=True, extra_field_updates=None,
                 extra_field_change_collection_updates=None,
                 extra_field_change_collection_like_regular=False,
                 *args, **kwargs):
        super(OrderedCollectionField, self).__init__(
            verbose_name=verbose_name, name=name, default=default,
            update_auto_now=update_auto_now, extra_field_updates=extra_field_updates,
            *args, **kwargs)

        if collection is None or not collection:
            raise TypeError(
                "{0} must have a collection, else use ordered_field".
                    format(self.__class__.__name__))

        if isinstance(collection, str):
            collection = (collection,)
        self.collection = collection

        # TODO: find some shorter names
        if extra_field_change_collection_updates is not None:
            self.extra_field_change_collection_updates = extra_field_change_collection_updates
        else:
            self.extra_field_change_collection_updates = {}

        if extra_field_change_collection_updates is None and \
                extra_field_change_collection_like_regular:
            self.extra_field_change_collection_updates = extra_field_updates

        self._collection_changed = None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["collection"] = self.collection
        if self.extra_field_change_collection_updates is not None:
            kwargs["extra_field_change_collection_updates"] = self.extra_field_change_collection_updates
        return name, path, args, kwargs

    #def contribute_to_class(self, cls, name, private_only=False):
    #    super(OrderedCollectionField, self).contribute_to_class(cls, name, private_only)

    def _get_collection(self, model_instance):
        filters = {}
        #if self.collection is not None:
        for field_name in self.collection:
            field = model_instance._meta.get_field(field_name)
            field_value = getattr(model_instance, field.attname)
            if field.null and field_value is None:
                filters['%s__isnull' % field.name] = True # Collection item is null
            else:
                filters[field.name] = field_value
        model = type(model_instance)
        if self.parent_link_name is not None:
            model = model._meta.get_field(self.parent_link_name).remote_field.model
        return model._default_manager.filter(**filters)

    def get_queryset(self, model_instance):
        return self._get_collection(model_instance)

    def update_on_save(self, sender, instance, created, **kwargs):
        collection_changed = self._collection_changed
        self._collection_changed = None

        current_value, updated_value = getattr(instance, self.get_cache_name())

        if current_value == updated_value and not collection_changed:
            return None # No positional changes, no need to update

        created = collection_changed or created
        super(OrderedCollectionField, self).update_on_save(
            sender, instance, created, (current_value, updated_value), **kwargs)

    def update_pre_save(self, sender, instance, **kwargs):
        self._collection_changed_then_delete_instance(instance)#, False)

        updates = None
        if self._collection_changed:
            # Self updates on collection change
            # TODO: rename to reflect self update
            updates = {}
            self._extra_updates(updates, self.extra_field_change_collection_updates)

        super(OrderedCollectionField, self).update_pre_save(
            sender, instance, updates=updates, **kwargs)

    def _collection_changed_then_delete_instance(self, model_instance):
        try:
            previous_instance = type(model_instance)._default_manager.get(pk=model_instance.pk)
        except models.ObjectDoesNotExist:
            return
        self._collection_changed = self._has_collection_changed(
            model_instance, previous_instance)
        if self._collection_changed:
            self._remove_from_collection(previous_instance)

    def _has_collection_changed(self, current_instance, previous_instance):
        """
        :param current_instance: Not None
        :param previous_instance: Not None
        :return: True if changed, else False
        """
        for field_name in self.collection:
            field = current_instance._meta.get_field(field_name)
            current_field_value = getattr(current_instance, field.attname)
            previous_field_value = getattr(previous_instance, field.attname)
            if previous_field_value != current_field_value:
                return True
        return False

    def _remove_from_collection(self, model_instance):
        updates = {self.name: models.F(self.name) - 1}
        self.extra_updates_on_change(model_instance, updates)
        current = getattr(model_instance, self.get_cache_name())[0]  # magic number :(
        queryset = self._get_collection(model_instance) # TODO: use get queryset ???
        queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def _get_cleaned_current_and_updated_values(self, add, model_instance, cache_name, values=None):
        current_value, updated_value = getattr(model_instance, cache_name)

        if self._collection_changed:
            if updated_value is None:
                # item changing position will be placed in current position if a new was not given
                updated_value = current_value
            current_value = None    # Has been removed from collection, so no current position

        return super(OrderedCollectionField, self)._get_cleaned_current_and_updated_values(
            add, model_instance, cache_name, (current_value, updated_value))


