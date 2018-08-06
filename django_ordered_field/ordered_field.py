from django.db import models
from django.db.models.fields.mixins import FieldCacheMixin
from django.core.exceptions import FieldDoesNotExist

from django_ordered_field.common import (get_values, generate_parent_link_name, extra_updates,
                                         auto_now_field_update, position_boundary_checks,
                                         get_cleaned_current_and_updated_values,
                                         order_is_not_changed, should_instance_be_updated)
from django_ordered_field.signals import add_signals_full


class OrderedField(models.IntegerField, FieldCacheMixin):

    description = "Position in an ordered table"

    def __init__(self, verbose_name=None, name=None, default=-1,
                 update_auto_now=True, extra_field_updates=None,
                 parent_link_name=None, *args, **kwargs):
        if 'unique' in kwargs:
            raise TypeError(
                "{0} can't have a unique constraint.". format(self.__class__.__name__))
        super(OrderedField, self).__init__(
            verbose_name=verbose_name, name=name, default=default, *args, **kwargs)
        self.update_auto_now = update_auto_now
        self.extra_field_updates = extra_field_updates if extra_field_updates is not None else {}
        self.parent_link_name = parent_link_name

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.update_auto_now is not None:
            kwargs["update_auto_now"] = self.update_auto_now
        if self.extra_field_updates is not None:
            kwargs["extra_field_updates"] = self.extra_field_updates
        if self.parent_link_name is not None:
            kwargs["parent_link_name"] = self.parent_link_name
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, private_only=False):
        super(OrderedField, self).contribute_to_class(cls, name, private_only)
        for constraint in cls._meta.unique_together:
            if self.name in constraint:
                raise TypeError(
                    "{0} can't be part of a unique constraint.".
                    format(self.__class__.__name__))
        setattr(cls, self.name, self)
        add_signals_full(cls, cls, self.name)

    def get_cache_name(self):
        return self.name + "_cache"

    def get_queryset(self, model_instance):
        return self.get_model(model_instance)._default_manager

    def get_model(self, model_instance):
        if model_instance is None:
            return
        if self.parent_link_name is not None:
            return self.get_parent_model(model_instance)
        return type(model_instance)

    def get_parent_model(self, model_instance):
        model = type(model_instance)
        try:
            return model._meta.get_field(self.parent_link_name).remote_field.model
        except FieldDoesNotExist:
            if generate_parent_link_name(model_instance) != self.parent_link_name:
                return model._meta.get_field(self.parent_link_name).remote_field.model
        return model

    def extra_updates_on_change(self, model_instance, updates):
        self.auto_now_field_update(model_instance, updates)
        extra_updates(updates, self.extra_field_updates)

    def auto_now_field_update(self, model_instance, updates):
        if self.update_auto_now:
            auto_now_field_update(model_instance, updates)

    def post_delete_handler(self, sender, instance, **kwargs):
        next_sibling = self.get_next_sibling(instance)
        current = getattr(instance, self.get_cache_name())[0]
        updates = {self.name: models.F(self.name) - 1}
        self.extra_updates_on_change(instance, updates)
        self.update_sibling_affected_by_delete(current, next_sibling, updates)

    def update_sibling_affected_by_delete(self, current, next_sibling, updates):
        try:
            queryset = self.get_queryset(next_sibling)
            queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)
        except AttributeError as e:
            return

    def get_next_sibling(self, model_instance):
        try:
            return self.get_queryset(model_instance).filter(
                **{'%s__gt' % self.name: getattr(model_instance, self.get_cache_name())[0]})[0]
        except IndexError:
            return None

    def pre_save_handler(self, sender, instance, values=None, updates=None, **kwargs):
        current_value, updated_value = get_values(instance, self.get_cache_name(), values)
        if order_is_not_changed(current_value, updated_value):
            return
        if should_instance_be_updated(instance):
            return
        if updates is None:
            # Inherited classes can send in custome update values
            # used for custom updates when item changes collection
            updates = {}
            extra_updates(updates, self.extra_field_updates)
        for key, value in updates.items():
            setattr(instance, key, value)

    def post_save_handler(self, sender, instance, created, values=None, **kwargs):
        current_value, updated_value = get_values(instance, self.get_cache_name(), values)
        if current_value == updated_value:
            return  # Order was not changed
        if current_value is None and created:
            current_value = -1
        setattr(instance, self.get_cache_name(), (updated_value, None))
        self.update_siblings_affected_by_save(instance, created, current_value, updated_value)

    def update_siblings_affected_by_save(self, instance, created, current_value, updated_value):
        queryset = self.get_queryset(instance).exclude(pk=instance.pk)
        updates = {}
        if created:
            # increment positions gte updated or node moved from another collection
            queryset = queryset.filter(**{'%s__gte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) + 1
        elif updated_value > current_value:
            # decrement positions gt current and lte updated
            queryset = queryset.filter(**{'%s__gt' % self.name: current_value,
                                          '%s__lte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) - 1
        else:
            # increment positions lt current and gte updated
            queryset = queryset.filter(**{'%s__lt' % self.name: current_value,
                                          '%s__gte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) + 1
        self.extra_updates_on_change(instance, updates)
        queryset.update(**updates)

    def pre_save(self, model_instance, add):
        return self.position_processing(model_instance, add)

    def position_processing(self, model_instance, add):
        cache_name = self.get_cache_name()

        current_value, updated_value = self.get_cleaned_current_and_updated_values(
            add, model_instance, cache_name)

        is_new = current_value is None  # NB: not the same as add
        max_position = self.get_max_position(model_instance, is_new)
        position = position_boundary_checks(updated_value, max_position)

        if add and position == max_position:
            setattr(model_instance, cache_name, (None, position))
        else:
            setattr(model_instance, cache_name, (current_value, position))
        return position

    def get_cleaned_current_and_updated_values(
            self, add, model_instance, cache_name, values=None):
        return get_cleaned_current_and_updated_values(add, model_instance, cache_name, values)

    def get_max_position(self, model_instance, is_new):
        current_count = self.get_queryset(model_instance).count()
        if is_new:
            return current_count
        return current_count - 1

    def __get__(self, instance, owner):
        current, updated = getattr(instance, self.get_cache_name())
        return current if updated is None else updated

    def __set__(self, instance, value):
        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            current, updated = getattr(instance, cache_name)
        except AttributeError:
            current, updated = value, None
        else:
            updated = value
        instance.__dict__[self.name] = value
        setattr(instance, cache_name, (current, updated))
