from django.db import models
from django.utils.timezone import now
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.signals import (post_delete, post_save, pre_delete)


class OrderedField(models.IntegerField, FieldCacheMixin):

    def __init__(self, verbose_name=None, name=None,
                 default=-1, update_auto_now=True,
                 *args, **kwargs):
        if 'unique' in kwargs:
            raise TypeError(
                "{0} can't have a unique constraint.".
                format(self.__class__.__name__))    # TODO; hit it
        super(OrderedField, self).__init__(
            verbose_name=verbose_name, name=name, default=default, *args, **kwargs)
        self.update_auto_now = update_auto_now

    def contribute_to_class(self, cls, name, private_only=False):
        super(OrderedField, self).contribute_to_class(cls, name, private_only)

        for constraint in cls._meta.unique_together:
            if self.name in constraint:
                raise TypeError(
                    "{0} can't be part of a unique constraint.".
                    format(self.__class__.__name__))    # TODO: Hit it
        setattr(cls, self.name, self)
        pre_delete.connect(self.prepare_delete, sender=cls)
        post_delete.connect(self.update_on_delete, sender=cls)
        post_save.connect(self.update_on_save, sender=cls)

    def get_cache_name(self):
        return self.name + "_cache"     # TODO: check if this si correct

    def get_queryset(self, model_instance):
        return type(model_instance)._default_manager.all()  # TODO: check all()

    def extra_updates_on_change(self, model_instance, updates):
        if self.update_auto_now:
            date_now = now()
            for field in model_instance._meta.get_fields():
                if getattr(field, 'auto_now', False):
                    updates[field.name] = date_now

    def get_next_sibling(self, model_instance):
        try:
            return self.get_queryset(model_instance). \
                filter(**{'%s__gt' % self.name: getattr(
                    model_instance, self.get_cache_name())[0]})[0]
        except IndexError:
            return None

    def prepare_delete(self, sender, instance, **kwargs):
        next_sibling = self.get_next_sibling(instance)
        if next_sibling:
            setattr(instance, '_next_sibling_pk', next_sibling.pk)
        else:
            setattr(instance, '_next_sibling_pk', None)
        pass

    def update_on_delete(self, sender, instance, **kwargs):
        next_sibling_pk = getattr(instance, '_next_sibling_pk', None)
        if next_sibling_pk:
            try:
                next_sibling = type(instance)._default_manager.get(pk=next_sibling_pk)
            except self.model.DoesNotExist:
                next_sibling = None  # TODO: try to hit this one
            if next_sibling:
                queryset = self.get_queryset(next_sibling)
                current = getattr(instance, self.get_cache_name())[0]
                updates = {self.name: models.F(self.name) - 1}
                self.extra_updates_on_change(instance, updates)
                queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)
        setattr(instance, '_next_sibling_pk', None)

    def update_on_save(self, sender, instance, created, values=None, **kwargs):
        current_value, updated_value = get_values(instance, self.get_cache_name(), values)

        if updated_value is None and created:
            updated_value = -1  # TODO: try to make a test that hit this one

        queryset = self.get_queryset(instance).exclude(pk=instance.pk)

        updates = {}
        self.extra_updates_on_change(instance, updates)

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

        queryset.update(**updates)
        setattr(instance, self.get_cache_name(), (updated_value, None))

    def pre_save(self, model_instance, add):
        cache_name = self.get_cache_name()

        current_value, updated_value = self._get_cleaned_current_and_updated_values(
            add, model_instance, cache_name)

        is_new = current_value is None  # NB: not the same as add
        min_position, max_position = self._get_max_min_positions(
            model_instance, is_new)

        position = position_boundary_checks(
            add, updated_value, min_position, max_position)

        if add and position == max_position:
            setattr(model_instance, cache_name, (position, None))
        else:
            setattr(model_instance, cache_name, (current_value, position))
        return position

    def _get_cleaned_current_and_updated_values(
            self, add, model_instance, cache_name, values=None):

        current_value, updated_value = get_values(model_instance, cache_name, values)

        if add and current_value is not None:
            # some cleanup if adding new record but current_value has an existing value
            if updated_value is None:
                updated_value = current_value
            current_value = None

        # existing instance, position not modified; no cleanup required
        if current_value is not None and updated_value is None:
            return current_value

        # if updated is still unknown set the object to the last position,
        # either it is a new object or collection has been changed
        if updated_value is None:
            updated_value = -1

        return current_value, updated_value

    def _get_max_min_positions(self, model_instance, is_new):
        current_count = self.get_queryset(model_instance).count()
        if is_new:
            max_position = current_count
        else:
            max_position = current_count - 1
        return 0, max_position

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        current, updated = getattr(instance, self.get_cache_name())
        return current if updated is None else updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            current, updated = getattr(instance, cache_name)
        except AttributeError:
            current, updated = value, None
        else:
            updated = value

        instance.__dict__[self.name] = value  # Django 1.10 fix for deferred fields #TODO: ???
        setattr(instance, cache_name, (current, updated))


def get_values(model_instance, cache_name, values=None):
    if values is None:
        return getattr(model_instance, cache_name)
    else:
        return values   # not safe from people sending in wrong stuff


def position_boundary_checks(add, current_value, min_position, max_position):
    if add and (current_value == -1 or current_value >= max_position):
        return max_position

    if max_position >= current_value >= min_position:
        # positive position; valid index
        return current_value
    elif current_value > max_position:
        # positive position; invalid index
        return max_position
    elif abs(current_value) <= (max_position + 1):
        # negative position; valid index
        # Add 1 to max_position to make this behave like a negative lists index.
        # -1 means the last position, not the last position minus 1
        return max_position + 1 + current_value
    # negative position; invalid index
    return min_position
